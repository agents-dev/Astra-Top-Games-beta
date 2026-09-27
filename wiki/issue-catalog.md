# Publish issue game reports

Open or edit an issue body with public HTTP(S) game links. Ignore non-URL text. Submit up to ten distinct links as a non-owner; apply no URL-count cap to the repository owner. Read the initial “I’m on it! This may take 10–30 minutes.” comment and Actions link before analysis.

Use the shared root catalog for every qualifying game. Keep `repository_url` empty when GitHub source cannot be verified and preserve the submitted URL in `links`. Match existing entries by repository identity or a recorded source link. Replace valid reports in place; retain old reports on analysis failure. Inspect `games/added.jsonl` for added/replaced outcomes.

Run analysis with read-only permissions and unpersisted checkout credentials. Transfer only the report JSON artifact to the concurrently waiting publisher. Revalidate and render with the publisher's trusted checkout. Create an issue-specific branch and a review PR. Read the PR or branch fallback link and per-game report in the issue comment. Leave merging to the reviewer.

Start SSH only for owner issues. Wait for publication on the same analysis worker, then hold its tunnel for thirty minutes, including after ordinary failures. Inspect its live records, logs, and processes by SSH; report verified results without waiting for the idle hold. Finish non-owner workers without a hold. Treat cancellation and runner loss as interruptions that cannot preserve SSH.

Configure `AGENTSWEB_SSH_PUBLIC_KEY` and permit Actions PR creation. Grant writes only to intake comments and the separate publishing job. Install OpenCode 1.18.31 for compatibility with the batch CLI. Keep each agent deadline at fifteen minutes and reserve time for publication and debugging within the hosted runner deadline. Inspect artifacts for partial results when the aggregate deadline expires.

Verify changes with real issues on the designated beta repository. Check sourced additions, source-unavailable additions, replacements, rejection reports, and non-owner limits. Inspect SSH and OpenCode while analysis runs. Report the generated PR and issue-comment links as soon as they appear.
