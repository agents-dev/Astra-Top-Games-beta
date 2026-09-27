# Astra-Top-Games instructions

## AgentsWeb runner testing

For SSH requests here, use the live AgentsWeb Actions runner and `~/.ssh/aiplay-agentsweb`; use `a2` only if named. Ask before starting a runner. Verify SSH before editing runner YAML.

In debug mode, SSH into the live Actions worker and inspect OpenCode records, logs, and processes. Report verified results without waiting for the 30-minute idle hold or Actions completion.

## OpenCode smoke command

Run `opencode run -m opencode/muse-spark-1.3-contributor-free hi` to verify the Muse Spark 1.3 model.

## OpenCode source

Use the local OpenCode source checkout at `../ChatGPT/opencode`. Refer to [the upstream repository](https://github.com/anomalyco/opencode) for its GitHub page.

## OpenCode test links

Copy every live OpenCode session URL printed by `scripts/test-oc.sh` immediately into a visible chat response as a clickable Markdown link. Include every run link again in the final response. Return after launch; inspect per-run `result.json` only when asked for outcomes.

## Wiki index

- Read [Issue catalog publishing](wiki/issue-catalog.md) before changing issue publication.

- Read [OpenCode batch testing](wiki/oc-batch-testing.md) before changing the batch runner.

## Verification

- Don't write or run unit tests, mock tests, or static analysis.
- Don't use mockups instead of a real end-to-end run.
- Don't ask the user to test or analyze; do it directly.
- Don't finish without running and analyzing the end-to-end flow.
