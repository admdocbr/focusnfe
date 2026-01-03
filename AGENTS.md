# FocusNFe - AGENTS.md

This document provides structured instructions for AI agents working on the FocusNFe repository.

## Project Context
FocusNFe is a robust, type-safe Python library for interacting with FocusNFe services (NFe, NFSe, etc.).

## Technical Stack
- **Language**: Python 3.11+
- **Package Manager**: `uv`
- **Core Libraries**: `pydantic` (v2), `requests`
- **Testing**: `pytest`, `pytest-cov`, `requests-mock`, `ruff`
- **Docstring Coverage**: `interrogate`
- **CI/CD**: GitHub Actions (defined in `.github/workflows/`)

## Setup & Tooling
- **ALWAYS** use `uv run` to execute scripts, tests, or tools.
- Never call tools directly (e.g., `pytest`) without the `uv run` prefix.
- Use `uv sync` to ensure the environment is up-to-date.

## Shared Commands
| Action | Project-Wide | File-Scoped (Efficient) |
| :--- | :--- | :--- |
| **Run Tests** | `uv run pytest` | `uv run pytest tests/test_path.py` |
| **Lint Check** | `uv run ruff check .` | `uv run ruff check path/to/file.py` |
| **Format** | `uv run ruff format .` | `uv run ruff format path/to/file.py` |
| **Doc Coverage** | `uv run interrogate src/focusnfe` | N/A |
| **Sync Docs** | `uv run python scripts/update_docs.py` | N/A |

## Development Rules

### 1. Pydantic Models
- Use `FocusNFeBaseModel` (from `focusnfe.models.common`) as the base class.
- Every field **MUST** have a `pydantic.Field` with a clear, descriptive `description`.
- Use modern Python type hints (`list[T]`, `X | Y`).
- **Validation**:
    - Use `validate_cpf_value` and `validate_cnpj_value` from `FocusNFeBaseModel` via `@field_validator`.
    - Input is automatically sanitized (strip whitespace, remove punctuation).

### 2. API Client
- Inherit from `BaseClient` in `focusnfe.base`.
- Use `requests.Session` for all calls.
- Return Pydantic models whenever possible.
- **Date Handling**: Use `FocusNFeJSONEncoder` for serialization.

### 3. Quality Standards
- **Coverage**: Maintain 100% code coverage and 100% docstring coverage.
- **Docstrings**: Use Google-style docstrings for all public methods and classes.

### 4. Documentation
- High-level docs are in `docs/`.
- The API Reference and Model tables are automatically synced from code via `scripts/update_docs.py`.
- Use `<!-- API_DOCS_START -->` and `<!-- API_DOCS_END -->` markers.

## Safety & Permissions
- **Allowed without prompt**:
    - Reading/listing files.
    - Running tests and linters (especially file-scoped ones).
    - Updating `task.md` and creating documentation artifacts.
- **Ask first**:
    - Adding or removing dependencies (e.g., `uv add`).
    - Modifying GitHub Actions workflows.
    - Massive refactors affecting more than 5 files.

## Dos and Don'ts
- **DO** verify all changes with `uv run pytest`.
- **DO** use file-scoped commands to save time and tokens.
- **DO** update `task.md` continuously.
- **DON'T** commit code that fails the build.
- **DON'T** hardcode Brazilian identifiers (CPF/CNPJ) in tests; use valid mock data.
- **DON'T** use `typing.List` or `typing.Dict`; use built-in `list` and `dict` types.
