# Reusable GitHub Actions Workflows

This repository contains reusable GitHub Actions workflows that can be shared across repositories in the fugue-project organization.

## PyPI Publish Workflow

A reusable workflow for publishing Python packages to PyPI using trusted publishing (OIDC) and the `uv` package manager.

### Usage

In your repository, create a workflow file (e.g., `.github/workflows/publish.yml`) with the following content:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    uses: fugue-project/.common/.github/workflows/pypi-publish.yml@master
```

That's it! The workflow will automatically use your repository name as the PyPI project name.

### Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `pypi-project-name` | PyPI project name for environment URL | No | Repository name |

### Custom PyPI Project Name

If your PyPI project name differs from your repository name, you can override it:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    uses: fugue-project/.common/.github/workflows/pypi-publish.yml@master
    with:
      pypi-project-name: 'custom-pypi-name'
```

### Prerequisites

For the workflow to work in your repository, ensure:

1. **PyPI Trusted Publishing**: Configure OIDC trusted publishing on PyPI for your package
   - Go to your PyPI project settings
   - Add a "trusted publisher" for GitHub Actions
   - Specify: `fugue-project`, your repository name, `publish.yml`, and `release` environment

2. **GitHub Environment**: Create a `release` environment in your repository settings
   - Go to Settings → Environments → New environment
   - Name it `release`
   - Add any required protection rules

3. **Repository Structure**: Your repository should have:
   - A `Makefile` with a `devenv` target
   - A `pyproject.toml` file with a `version` field

### How It Works

1. Triggers on push of tags matching `v*`
2. Checks out the calling repository's code
3. Checks out the common workflows repository (for validation script)
4. Sets up the `uv` package manager with Python 3.11
5. Runs `make devenv` to setup development environment
6. Validates the release tag matches version in `pyproject.toml`
7. Builds the package using `uv build`
8. Publishes to PyPI using `uv publish` with OIDC authentication

### Release Tag Validation

The workflow automatically validates that your git tag matches the version in `pyproject.toml`. The validation script:

- Extracts the version from your `pyproject.toml` file
- Compares it with the git tag (strips `v` prefix if present)
- Fails the build if there's a mismatch

**Example**: If your `pyproject.toml` has `version = "1.2.3"`, the tag must be either `v1.2.3` or `1.2.3`.

The validation script is included in this common repository, so you don't need to maintain it in each project.

### Benefits

- **Zero Configuration**: Works out of the box - just reference the workflow and you're done
- **Reduced Duplication**: Single source of truth for PyPI publishing logic and validation
- **Consistency**: All projects use the same tested workflow
- **Easy Updates**: Fix bugs or add features in one place
- **Security**: Uses OIDC trusted publishing (no stored credentials)
