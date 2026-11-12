# Evidence

Before changing behavior, identify the observable result that would satisfy the user's request. Accept the work by checking that result in the target application, client, integration, or generated artifact.

For each material promise, verify the corresponding scenario and relevant mode. A successful command, valid configuration, passing tests, or a subagent's report alone does not prove that the promised result reached its consumer. Treat an unexpectedly easy or fast success as a reason to check for a silent no-op.

If a change affects behavior, create or update tests according to project rules using local project tools. If testing is not configured or a test is not appropriate, say so explicitly in the result.

Run the project's mandatory checks and relevant checks for the changed area, including formatters and linters where provided. Run a build when required by project rules or needed to verify the consequences of the change; do not default to a full repository build for every task.

Required checks must pass before reporting the result as verified. If a check fails or cannot run, investigate and report the cause, distinguishing an implementation failure from an environment or access blocker. Continue independent work within the authorized scope; handle significant changes of approach under the autonomy rules. A draft PR can expose a blocker, but the corresponding acceptance criterion remains unverified.

After UI changes, open the app or Storybook in a browser and capture screenshots. Use a non-default dev server port to avoid colliding with the user's server.

Stop dev servers and background processes before finishing.

For each material acceptance criterion, provide observable evidence: changed tests and their run results, relevant check output, screenshots of the required UI state, actual integration run results, or excerpts and readbacks of generated artifacts. Choose evidence that proves the promised behavior; do not substitute a list of commands for their outcomes.

Include this evidence in the draft PR and summarize it in the final response with links to the PR and relevant artifacts. Clearly separate verified results, failed checks, unavailable checks, and remaining limitations. Do not report a partially completed installation or integration as complete.
