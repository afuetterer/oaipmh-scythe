# justfile
# Ref: https://just.systems/man/en/
# ------------------------------------------------------------------------------

export UV_LOCKED := "true" # do not update the lockfile during `uv sync` and `uv run` commands
export UV_EXCLUDE_NEWER := "1 week" # ignore packages published in the last week

_default:
    @just --list --unsorted

# Sync the project's dependencies with the environment.
sync:
    uv sync

# Sync only documentation dependencies with the environment.
sync-docs:
    uv sync --group=docs

# Get the current project version
@project-version:
    uv version | awk '{print $2}'

prek := "prek run --all-files --color=always --show-diff-on-failure"

# Run all all prek hooks and pytest tests
qa: check test

# Run all prek hooks except mypy
[group('lint')]
lint:
    uv run {{ prek }} --skip mypy

# Run only mypy through prek
[group('lint')]
typecheck:
    uv run {{ prek }} mypy

# Run all prek hooks including mypy
[group('lint')]
check:
    uv run {{ prek }}

# Run pytest tests
[group('test')]
test:
    uv run pytest tests

# Run pytest tests with coverage
[group('test')]
cov:
    uv run pytest --cov=src

# Generate coverage report in markdown format
[group('test')]
cov-report-markdown:
    uv run python -m coverage report --format=markdown > coverage.md

# Get total coverage percentage
[group('test')]
@cov-total:
    uv run python -m coverage json --quiet
    uv run python -c "import json;print(json.load(open('coverage.json'))['totals']['percent_covered_display'])"

config := "--config-file=docs/mkdocs.yml"

# Build the documentation site
[group('docs')]
docs-build:
    uv run mkdocs build {{ config }}

# Serve documentation locally with live reload
[group('docs')]
docs-serve:
    uv run mkdocs serve {{ config }} --verbose

# Deploy documentation to GitHub Pages using mike
[group('docs')]
docs-deploy:
    uv run mike deploy {{ config }} --push --update-aliases $(just project-version) latest
