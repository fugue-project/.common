# Lint Action

A composite action for running code linting on Python projects using pre-commit and the `uv` package manager.

## Usage

In your repository, create a workflow file (e.g., `.github/workflows/lint.yml`) with the following content:

```yaml
name: Lint

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: fugue-project/.common/.github/actions/lint@main
```

That's it! The action will automatically checkout your repo, install dependencies, and run pre-commit.

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python version to use | No | `3.12` |

## Example with Custom Python Version

```yaml
name: Lint

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: fugue-project/.common/.github/actions/lint@main
        with:
          python-version: '3.11'
```

## Prerequisites

Your repository should have:
- A `Makefile` with a `devenv` target (to install dependencies including pre-commit)

## How It Works

1. Checks out the calling repository's code
2. Sets up `uv` package manager with the specified Python version
3. Runs `make devenv` to install dependencies
4. Runs `uv run pre-commit run --all-files` using the bundled `.pre-commit-config.yml`

## Self-Contained Configuration

The pre-commit configuration is bundled with this action. When you reference the action at a specific ref (e.g., `@main` or `@v1.0.0`), you automatically get the configuration from that same ref.

## Benefits

- **Simple**: Just one line to add linting to your project
- **Version-Locked**: Config travels with the action at the same git ref
- **Consistent**: All projects use the same linting rules
- **Zero Config**: No need to maintain pre-commit config in each repo
