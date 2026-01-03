# FocusNFe Library - Agent Instructions

This document provides context and rules for AI agents working on this repository.

## Technical Stack
- **Language**: Python 3.11+
- **Package Manager**: `uv`
- **Core Libraries**: `pydantic` (v2), `requests`
- **Testing**: `pytest`, `pytest-cov`, `requests-mock`, `ruff`
- **Docstring Coverage**: `interrogate`
- **CI/CD**: GitHub Actions (defined in `.github/workflows/`)
- **Lifecycle**: `pre-commit` hooks, `dependabot` (weekly)

## Project Rules
0. **Tooling**:
    - ALWAYS use `uv run` to execute scripts, tests, or tools (e.g., `pytest`, `ruff`, `interrogate`).
    - Use `uv sync` for dependency management.
    - Never call tools directly (e.g., `pytest`) without the `uv run` prefix unless `uv` is not applicable.

1. **Pydantic Models**: 
    - Always use `FocusNFeBaseModel` (from `focusnfe.models.common`) as the base class.
    - Every field MUST have a `pydantic.Field` with a clear, descriptive `description`.
    - Use `populate_by_name=True` (configured in the base model).
    - Favor modern Python type hints (e.g., `list[T]`, `dict[K, V]`, `X | Y`) over `typing` aliases where possible.
2. **API Client**:
    - Inherit from `BaseClient` in `focusnfe.base`.
    - Use `requests.Session` for all calls.
    - Return Pydantic models whenever possible.
    - **Date Handling**: Use the custom `FocusNFeJSONEncoder` for serialization.
    - **Error Handling**: `FocusNFeError` provides human-readable messages from API responses.
3. **Quality Standards**:
    - Maintain **100% code coverage** (verified by `pytest-cov`).
    - Maintain **100% docstring coverage** (verified by `interrogate`).
    - Use Google-style or similar descriptive docstrings for all classes and public methods.
4. **Documentation**:
    - High-level docs are in `docs/` (e.g., `docs/nfe.md`).
    - **Automated Sync**: The API Reference and Model tables in `docs/*.md` are automatically updated from code via `scripts/update_docs.py`.
    - Always add `<!-- API_DOCS_START -->` and `<!-- API_DOCS_END -->` markers when creating new service documentation.

## Common Commands
- Run tests: `uv run pytest --cov=src/focusnfe tests/`
- Lint/Format check: `uv run ruff check .` and `uv run ruff format --check .`
- Auto-fix/Format: `uv run ruff check --fix .` and `uv run ruff format .`
- Docstring coverage: `uv run interrogate src/focusnfe`
- Sync documentation: `uv run python scripts/update_docs.py`
- Build package: `uv build`
- Release Guide: See `docs/RELEASE.md` for versioning and submission steps.
