import path from 'node:path';
import { hookCommand, jsonFileUpdate, readJsonFile, replaceManagedCommandHookGroup } from '../common.mjs';

export function render(specs, context) {
  const targetPath = path.join(context.home, '.claude/settings.json');
  const config = readJsonFile(targetPath, { hooks: {} }, context);
  config.hooks ??= {};

  for (const spec of specs) {
    config.hooks.PreToolUse = replaceManagedCommandHookGroup(
      config.hooks.PreToolUse,
      spec,
      {
        matcher: 'Bash',
        hooks: [
          {
            type: 'command',
            command: hookCommand(spec, 'claude'),
            timeout: spec.timeout,
          },
        ],
      },
    );
  }

  return [jsonFileUpdate(targetPath, config)];
}
