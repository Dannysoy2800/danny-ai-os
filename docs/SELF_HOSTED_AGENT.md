# Self-Hosted Agent Skills

## Delegation model

Skills are entry points, not claims that a task has already been executed. The
built-in `research`, `verify`, and `code` skills use an injected
`FreeFirstDelegator` to hand work to registered tool adapters.

### Free-first policy
- Local/self-hosted adapters are preferred, then free adapters.
- Paid adapters are excluded by the delegator; there is no automatic paid fallback.
- Retries are bounded to a maximum of three attempts per adapter.
- Empty outputs and tool failures do not count as success.
- If no local/free adapter is configured, the task reports `blocked` honestly.
- Adapter exception messages are not copied into user-facing error messages.

### Quality gate
An optional independent reviewer callback can accept/reject each adapter result.
A result only reports `quality_checked=True` when a reviewer is configured and
accepts it. Without a reviewer, the output may complete but is explicitly marked
as not quality-checked. A production deployment should supply a reviewer that
checks factual claims against sources and runs appropriate tests for code changes.

### Built-in skills
- `research` — delegate research to a configured adapter.
- `verify` — delegate verification to a configured adapter/reviewer.
- `code` — delegate coding/build work to a configured adapter.

## Current limitations

No external tool adapter is enabled by default. This repository change supplies
the routing interface and testable safety behavior; it does not claim that
Ollama, Firecrawl, a hosted bot, or a coding agent is already connected. Add and
test adapters separately, using environment-based credentials and least-privilege
permissions. Human approval remains required for merges, deployments, purchases,
and other consequential actions.

No credentials are stored in source code.
