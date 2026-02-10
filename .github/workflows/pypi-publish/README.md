# PyPI Publish Workflow

A reusable workflow for publishing Python packages to PyPI using API token authentication and the `uv` package manager.

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
    uses: fugue-project/.common/.github/workflows/pypi-publish/workflow.yml@main
    secrets:
      PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

That's it! The workflow will automatically use your repository name as the PyPI project name.

### Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `pypi-project-name` | PyPI project name for environment URL | No | Repository name |

### Secrets

| Secret | Description | Required |
|--------|-------------|----------|
| `PYPI_TOKEN` | PyPI API token for authentication | Yes |

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
    uses: fugue-project/.common/.github/workflows/pypi-publish/workflow.yml@main
    with:
      pypi-project-name: 'custom-pypi-name'
    secrets:
      PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

### Prerequisites

For the workflow to work in your repository, ensure:

1. **PyPI API Token**: Create and configure a PyPI API token
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token (can be scoped to a specific project or account-wide)
   - Add the token to your repository secrets:
     - Go to Settings → Secrets and variables → Actions
     - Create a new secret named `PYPI_TOKEN`
     - Paste your PyPI API token as the value

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
8. Publishes to PyPI using `uv publish` with API token authentication

### Release Tag Validation

The workflow automatically validates that your git tag matches the version in `pyproject.toml`. The validation script:

- Extracts the version from your `pyproject.toml` file
- Compares it with the git tag (strips `v` prefix if present)
- Fails the build if there's a mismatch

**Example**: If your `pyproject.toml` has `version = "1.2.3"`, the tag must be either `v1.2.3` or `1.2.3`.

The validation script is included in this common repository, so you don't need to maintain it in each project.

### Benefits

- **Zero Configuration**: Works out of the box - just reference the workflow and add your PyPI token
- **Reduced Duplication**: Single source of truth for PyPI publishing logic and validation
- **Consistency**: All projects use the same tested workflow
- **Easy Updates**: Fix bugs or add features in one place
- **Security**: Uses GitHub Secrets to securely store your PyPI API token
