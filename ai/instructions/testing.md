# Verification

Run formatters for changed code whenever the project provides them.

If a change affects behavior, create or update tests according to project rules using local project tools. If testing is not configured or a test is not appropriate, say so explicitly in the result.

After changes, run relevant linters, formatters, unit tests, integration tests, and available smoke checks for external dependencies. Do not run full builds by default.

For broad changes or changes touching external integrations, suggest available E2E tests before running them.

If checks fail, investigate the cause. If the failure is unrelated or the next step is unclear, report the cause and ask the user how to proceed.

After UI changes, open the app or Storybook in a browser and capture screenshots. Use a non-default dev server port to avoid colliding with the user's server.

Stop dev servers and background processes before finishing.
