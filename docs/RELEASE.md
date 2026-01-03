# Release Process

This document describes the steps required to release a new version of the `focusnfe` library.

## 1. Preparation

Before releasing, ensure the quality of the codebase:

```bash
# Run tests and verify 100% coverage
uv run pytest --cov=src/focusnfe tests/

# Run linting and formatting checks
uv run ruff check .
uv run ruff format --check .
```

## 2. Update Version

Update the version number in `pyproject.toml`. We follow [Semantic Versioning](https://semver.org/).

1. Open `pyproject.toml`.
2. Change the `version` field (e.g., from `0.1.0` to `0.2.0`).

## 3. Commit the Change

Commit the version bump to the repository:

```bash
git add pyproject.toml
git commit -m "chore: bump version to v0.x.x"
```

## 4. Create a Git Tag

Create a tag that matches the version in `pyproject.toml`. This tag must start with `v`.

```bash
git tag v0.x.x
```

## 5. Push to GitHub

Push the commit and the tag to the `main` branch. This will trigger the automated CI/CD workflows.

```bash
git push origin main
git push origin v0.x.x
```

## 6. Automated Workflows

Once pushed, GitHub Actions will:
- **Test & Lint**: Verify the code on multiple Python versions.
- **Publish**: Automatically build the package and upload it to PyPI (via the `publish.yml` workflow).

> [!IMPORTANT]
> Ensure that the "Trusted Publishing" setup is completed on PyPI for this repository before the first release.
