import path from 'node:path';
import { hookCommand, jsonFileUpdate, readJsonFile, replaceManagedCommandHook } from '../common.mjs';

export function render(specs, context) {
  const targetPath = path.join(context.home, '.cursor/hooks.json');
  const config = readJsonFile(targetPath, { hooks: {} }, context);
  config.hooks ??= {};

  for (const spec of specs) {
    config.hooks.beforeShellExecution = replaceManagedCommandHook(
      config.hooks.beforeShellExecution,
      spec,
      {
        command: hookCommand(spec, 'cursor'),
        timeout: spec.timeout,
        matcher: spec.matcher,
      },
    );
  }

  return [jsonFileUpdate(targetPath, config)];
}
