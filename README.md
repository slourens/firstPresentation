# firstPresentation

## Getting started

Set up Python 3.11+ with the tooling from `requirements-dev.txt`, then use the Makefile targets (e.g., `make dev`, `make test-unit`) to run services and tests locally.

If dependency installation fails because of corporate proxies or limited internet access, follow the guidance in [docs/proxy.md](docs/proxy.md) to configure `pip`, Docker, and environment variables so the test targets can run successfully.

### Running tests in restricted environments (including Codex)

If you cannot download dependencies (for example, due to a strict proxy), the repo includes lightweight compatibility shims for FastAPI, Pydantic, and JSON Schema validation so `pytest` still runs. Simply execute:

```
python -m pytest
```

The stubs only cover the small surface used in the sample services (routing decorators, simple models, and basic schema checks). For real service behavior, install the full dependencies or run `make dev` once network access is available.
