# Self-Hosted Agent Skills

## Current foundation

The runtime is provider-agnostic. Skills are Python callables, while model/provider routing is a separate layer.

### Built-in skills
- research — research task entry point
- verify — source/result verification entry point
- code — coding/build task entry point

### Routing policy
Providers are ordered by ascending priority, so local/self-hosted providers can be placed first. The router retries each healthy provider up to three times before failing over.

### Next integration points
1. Add an Ollama provider.
2. Add OpenAI-compatible API provider support.
3. Add Firecrawl research adapter.
4. Add persistent memory and audit logging.
5. Connect LangGraph orchestration to these primitives.

No credentials are stored in source code.
