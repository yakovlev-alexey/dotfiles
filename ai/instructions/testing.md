# Verification

Before changing behavior, identify the observable result that would satisfy the user's request. Accept the work by checking that result in the target application, client, integration, or generated artifact.

For each material promise, verify the corresponding scenario and relevant mode. A successful command, valid configuration, passing tests, or a subagent's report alone does not prove that the promised result reached its consumer. Treat an unexpectedly easy or fast success as a reason to check for a silent no-op.

Run formatters for changed code whenever the project provides them.

If a change affects behavior, create or update tests according to project rules using local project tools. If testing is not configured or a test is not appropriate, say so explicitly in the result.

After changes, run relevant linters, formatters, unit tests, integration tests, and available smoke checks for external dependencies. Do not run full builds by default.

For broad changes or changes touching external integrations, suggest available E2E tests before running them.

If checks fail, investigate and report the cause. Continue independent work within the authorized scope; handle unexpected obstacles and significant changes of approach under the autonomy rules.

After UI changes, open the app or Storybook in a browser and capture screenshots. Use a non-default dev server port to avoid colliding with the user's server.

Stop dev servers and background processes before finishing.

In the final result, state what was verified and identify any material promise or boundary that remains unverified. Do not report a partially completed installation or integration as complete.
