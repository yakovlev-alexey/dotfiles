import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { render as renderClaude } from './clients/claude.mjs';
import { render as renderCodex } from './clients/codex.mjs';
import { render as renderCursor } from './clients/cursor.mjs';
import { render as renderOpenCode } from './clients/opencode.mjs';
import { writeUpdates } from './common.mjs';

const [repoRootArg, modeArg = 'install', homeArg] = process.argv.slice(2);
if (!repoRootArg) throw new Error('install-agent-hooks: missing repo root argument');

const repoRoot = path.resolve(repoRootArg);
const mode = modeArg;
const home = path.resolve(homeArg ?? process.env.DOTFILES_AGENT_HOOKS_HOME ?? os.homedir());
const knownClients = new Set(['cursor', 'codex', 'claude', 'opencode']);
const clientRenderers = {
  cursor: renderCursor,
  codex: renderCodex,
  claude: renderClaude,
  opencode: renderOpenCode,
};

if (!['install', 'check', 'dry-run'].includes(mode)) {
  throw new Error(`install-agent-hooks: unknown mode: ${mode}`);
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function findHookManifestPaths(dir) {
  if (!fs.existsSync(dir)) return [];

  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const nested = entries
    .filter((entry) => entry.isDirectory())
    .flatMap((entry) => findHookManifestPaths(path.join(dir, entry.name)));

  const hookName = path.basename(dir);
  const manifestPath = path.join(dir, `${hookName}.json`);
  return fs.existsSync(manifestPath) ? [manifestPath, ...nested] : nested;
}

function loadHookSpecs() {
  const hooksRoot = path.join(repoRoot, 'ai/hooks');
  const specs = [];

  for (const manifestPath of findHookManifestPaths(hooksRoot).sort()) {
    const hookDir = path.dirname(manifestPath);
    const manifest = readJson(manifestPath);
    validateManifest(manifest, manifestPath);
    if (!manifest.enabled) continue;

    const handlerPath = path.join(hookDir, manifest.handler);
    if (!fs.existsSync(handlerPath)) {
      throw new Error(`install-agent-hooks: missing handler for ${manifest.id}: ${handlerPath}`);
    }

    specs.push({
      ...manifest,
      hookDir,
      manifestPath,
      handlerPath,
    });
  }

  return specs;
}

function validateManifest(manifest, manifestPath) {
  for (const key of ['id', 'enabled', 'event', 'handler', 'matcher', 'timeout', 'clients']) {
    if (!(key in manifest)) throw new Error(`install-agent-hooks: ${manifestPath} missing ${key}`);
  }
  if (manifest.event !== 'shell.before') {
    throw new Error(`install-agent-hooks: ${manifestPath} unsupported event: ${manifest.event}`);
  }
  if (!Array.isArray(manifest.clients) || manifest.clients.length === 0) {
    throw new Error(`install-agent-hooks: ${manifestPath} clients must be a non-empty array`);
  }
  for (const client of manifest.clients) {
    if (!knownClients.has(client)) {
      throw new Error(`install-agent-hooks: ${manifestPath} unknown client: ${client}`);
    }
  }
  if (!Number.isInteger(manifest.timeout) || manifest.timeout <= 0) {
    throw new Error(`install-agent-hooks: ${manifestPath} timeout must be a positive integer`);
  }
}

function renderUpdates(specs) {
  const updates = [];
  const context = {
    home,
    repoRoot,
    readExisting: mode !== 'check',
  };

  for (const client of Object.keys(clientRenderers)) {
    const clientSpecs = specs.filter((spec) => spec.clients.includes(client));
    if (clientSpecs.length === 0) continue;
    updates.push(...clientRenderers[client](clientSpecs, context));
  }

  return updates;
}

const specs = loadHookSpecs();
const updates = renderUpdates(specs);

if (mode === 'install') {
  writeUpdates(updates);
  for (const update of updates) console.log(`install-agent-hooks: synced ${update.targetPath}`);
} else {
  for (const update of updates) console.log(`install-agent-hooks: would sync ${update.targetPath}`);
  console.log(`install-agent-hooks: ${mode} ok`);
}
