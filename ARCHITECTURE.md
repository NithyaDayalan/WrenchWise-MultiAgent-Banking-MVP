# Architecture and design decisions

## Request lifecycle

1. User chooses a fictional customer and enters a natural-language request.
2. `Supervisor.handle()` performs simple keyword-based intent classification.
3. The Supervisor calls one or more specialized agent methods.
4. Agents access simulated records and return structured dictionaries.
5. `llm.natural_language_response()` creates a grounded answer. It uses deterministic formatting by default; Gemini is optional.
6. The UI renders the answer, execution trace and JSON results.

## Why this MVP design?

- **Fast to run:** Streamlit avoids a separate frontend build.
- **Explainable:** separate agent classes and visible execution traces make behavior easy to inspect.
- **Safe by default:** no real banking integration and no real transaction execution.
- **Graceful fallback:** core use cases work without an LLM API key.
- **Expandable:** agents can later be exposed as REST APIs or MCP tools; routing can later use structured model output.

## Current limitations

The Supervisor uses keyword rules rather than an LLM-based router. Fraud detection and loan eligibility are rule-based simulations, not trained ML models. The demo has no production authentication, persistent database, or real external services.
