import fs from 'node:fs';
import path from 'node:path';

export function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

export function readJsonFile(filePath, fallback, { readExisting = true } = {}) {
  if (!readExisting || !fs.existsSync(filePath)) return structuredClone(fallback);
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    throw new Error(`install-agent-hooks: invalid JSON in ${filePath}: ${error.message}`);
  }
}

export function jsonFileUpdate(targetPath, value) {
  return {
    targetPath,
    content: JSON.stringify(value, null, 2) + '\n',
  };
}

export function shellQuote(value) {
  return `'${String(value).replaceAll("'", "'\"'\"'")}'`;
}

export function hookCommand(spec, client, options = {}) {
  const args = [
    'python3',
    shellQuote(spec.handlerPath),
    '--client',
    client,
    '--hook-id',
    spec.id,
  ];
  if (options.format) args.push('--format', options.format);
  return args.join(' ');
}

export function isManagedCommandHook(value, spec) {
  return Boolean(value?.command && String(value.command).includes(`--hook-id ${spec.id}`));
}

export function replaceManagedCommandHook(hooks, spec, hook) {
  return [...(hooks ?? []).filter((candidate) => !isManagedCommandHook(candidate, spec)), hook];
}

export function replaceManagedCommandHookGroup(groups, spec, group) {
  const retained = [];
  for (const candidate of groups ?? []) {
    const hooks = (candidate.hooks ?? []).filter((hook) => !isManagedCommandHook(hook, spec));
    if (hooks.length > 0) retained.push({ ...candidate, hooks });
  }
  retained.push(group);
  return retained;
}

export function writeUpdates(updates) {
  for (const update of updates) {
    ensureDir(path.dirname(update.targetPath));
    fs.writeFileSync(update.targetPath, update.content);
  }
}
