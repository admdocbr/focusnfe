# FocusNFe Library - Agent Instructions

This document provides context and rules for AI agents working on this repository.

## Technical Stack
- **Language**: Python 3.11+
- **Package Manager**: `uv`
- **Core Libraries**: `pydantic` (v2), `requests`
- **Testing**: `pytest`, `pytest-cov`, `requests-mock`, `ruff`
- **CI/CD**: GitHub Actions (defined in `.github/workflows/`)

## Project Rules
1. **Pydantic Models**: 
    - Always use `FocusNFeBaseModel` (from `focusnfe.models.common`) as the base class.
    - Every field MUST have a `pydantic.Field` with a clear, descriptive `description`.
    - Use `populate_by_name=True` (configured in the base model).
2. **API Client**:
    - Inherit from `BaseClient` in `focusnfe.base`.
    - Use `requests.Session` for all calls.
    - Return Pydantic models whenever possible.
3. **Test Coverage**:
    - Maintain **100% code coverage**.
    - Use `requests-mock` to isolate tests from the real API.
4. **Documentation**:
    - Keep the root `README.md` generic.
    - Put sub-type specific documentation in the `docs/` folder (e.g., `docs/nfe.md`).

## Common Commands
- Run tests: `uv run pytest --cov=src/focusnfe tests/`
- Lint/Format check: `uv run ruff check .` and `uv run ruff format --check .`
- Auto-fix/Format: `uv run ruff check --fix .` and `uv run ruff format .`
- Build package: `uv build`
- Sync dependencies: `uv sync`
