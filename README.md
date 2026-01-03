# FocusNFe Python Library

A robust, type-safe Python library for interacting with [FocusNFe](https://focusnfe.com.br/) services.

## Features

- **Pydantic Models**: All requests and responses are validated using Pydantic.
- **Requests Session**: Uses `requests.Session` for efficient connection pooling.
- **High Test Coverage**: 100% test coverage with `pytest` and `requests-mock`.
- **Sandbox/Production Support**: Easily switch between environments.

## Installation

This project uses `uv` for package management.

```bash
uv add focusnfe
```

## Quick Start

```python
from focusnfe import FocusNFe

# Sandbox (default)
client = FocusNFe(api_token="your_sandbox_token")

# Production
client = FocusNFe(api_token="your_production_token", sandbox=False)
```

## Services Documentation

For detailed examples and model information for each service, see:

- [NF-e (Product Invoices)](docs/nfe.md)
- [NFS-e (Service Invoices)](docs/nfse.md)

## Development

### Running Tests

```bash
uv run pytest --cov=src/focusnfe tests/
```

### Project Structure

- `src/focusnfe/client.py`: Main client class.
- `src/focusnfe/base.py`: Base API request handler.
- `src/focusnfe/models/`: Pydantic models for data validation.
- `tests/`: Comprehensive test suite.
- `docs/`: Detailed service documentation.
