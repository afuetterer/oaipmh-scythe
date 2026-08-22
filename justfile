# justfile
# Ref: https://just.systems/man/en/
# ------------------------------------------------------------------------------

alias t := test
alias lint := check

export UV_LOCKED := "true" # do not update the lockfile during `uv sync` and `uv run` commands

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

# Run all all prek hooks and pytest tests
qa: check test

# Run all prek hooks
[group('lint')]
check *args:
    uv run prek run --all-files --color=always --show-diff-on-failure {{ args }}

# Run pytest tests
[group('test')]
test *args:
    uv run pytest {{ args }}

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

# Generate a changelog using git-cliff
[group('docs')]
changelog:
     uvx git-cliff --config=.github/templates/changelog.toml --output

mkdocs := "uv run --group=docs mkdocs"
config := "--config-file=docs/mkdocs.yml"

# Build the documentation site
[group('docs')]
docs-build:
    {{ mkdocs }} build {{ config }}

# Serve documentation locally with live reload
[group('docs')]
docs-serve:
    {{ mkdocs }} serve {{ config }} --verbose

# Deploy documentation to GitHub Pages using mike
[group('docs')]
docs-deploy:
    uv run --group=docs mike deploy {{ config }} --push --update-aliases $(just project-version) latest
