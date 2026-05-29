import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const [repoRoot, profile] = process.argv.slice(2);
const home = os.homedir();
const manifestPath = path.join(repoRoot, 'ai/mcp.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function expand(value) {
  if (typeof value !== 'string') return value;
  let result = value;
  if (result === '~') result = home;
  if (result.startsWith('~/')) result = home + result.slice(1);
  result = result.replaceAll('$HOME', home);
  result = result.replace(/\$\{([A-Z_][A-Z0-9_]*)\}/g, (_, name) => {
    const envValue = process.env[name];
    if (!envValue) throw new Error(`install-mcp: missing environment variable: ${name}`);
    return envValue;
  });
  return result;
}

function enabledFor(server, client) {
  if (!server.enabled) return false;
  const clientConfig = server.clients?.[client];
  return clientConfig?.enabled !== false;
}

function clientName(name, server, client) {
  return server.clients?.[client]?.name ?? name;
}

function localCommand(server) {
  if (server.transport !== 'local') throw new Error(`unsupported transport: ${server.transport}`);
  return {
    command: expand(server.command),
    args: (server.args ?? []).map(expand),
  };
}

const entries = Object.entries(manifest);

const cursorServers = {};
for (const [name, server] of entries) {
  if (!enabledFor(server, 'cursor')) continue;
  cursorServers[clientName(name, server, 'cursor')] = localCommand(server);
}
ensureDir(path.join(home, '.cursor'));
fs.writeFileSync(path.join(home, '.cursor/mcp.json'), JSON.stringify({ mcpServers: cursorServers }, null, 2) + '\n');

const opencodeTemplatePath = path.join(repoRoot, 'opencode/opencode.template.json');
const opencodeConfig = JSON.parse(fs.readFileSync(opencodeTemplatePath, 'utf8'));
opencodeConfig.mcp = {};
for (const [name, server] of entries) {
  if (!enabledFor(server, 'opencode')) continue;
  const command = localCommand(server);
  opencodeConfig.mcp[clientName(name, server, 'opencode')] = {
    enabled: true,
    type: 'local',
    command: [command.command, ...command.args],
  };
}
ensureDir(path.join(home, '.config/opencode'));
fs.writeFileSync(path.join(home, '.config/opencode/opencode.json'), JSON.stringify(opencodeConfig, null, 2) + '\n');

const templateCandidates = [
  path.join(repoRoot, `codex/config.${profile}.template.toml`),
  path.join(repoRoot, 'codex/config.template.toml'),
];
const codexTemplatePath = templateCandidates.find((candidate) => fs.existsSync(candidate));
if (!codexTemplatePath) throw new Error('install-mcp: missing Codex config template');
const codexTemplate = fs.readFileSync(codexTemplatePath, 'utf8');
const marker = '# __MCP_SERVERS__';
if (!codexTemplate.includes(marker)) throw new Error(`install-mcp: missing marker in ${codexTemplatePath}`);

function tomlString(value) {
  return JSON.stringify(value);
}

function tomlArray(items) {
  return `[${items.map(tomlString).join(', ')}]`;
}

const codexBlocks = [];
for (const [name, server] of entries) {
  if (!enabledFor(server, 'codex')) continue;
  const command = localCommand(server);
  const codexName = clientName(name, server, 'codex');
  codexBlocks.push([
    `[mcp_servers.${codexName}]`,
    `command = ${tomlString(command.command)}`,
    command.args.length ? `args = ${tomlArray(command.args)}` : '',
  ].filter(Boolean).join('\n'));
}

ensureDir(path.join(home, '.codex'));
fs.writeFileSync(path.join(home, '.codex/config.toml'), codexTemplate.replace(marker, codexBlocks.join('\n\n')));

console.log('install-mcp: synced ~/.cursor/mcp.json');
console.log('install-mcp: synced ~/.config/opencode/opencode.json');
console.log('install-mcp: synced ~/.codex/config.toml');
