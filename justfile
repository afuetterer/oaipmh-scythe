# justfile
# Ref: https://just.systems/man/en/
# ------------------------------------------------------------------------------

export UV_LOCKED := "true"

_default:
    @just --list --unsorted

sync:
    uv sync

sync-docs:
    uv sync --group=docs

@project-version:
    uv version | awk '{print $2}'

pre-commit := "pre-commit run --all-files --color=always --show-diff-on-failure"

[group('lint')]
lint:
    SKIP=mypy uv run {{ pre-commit }}

[group('lint')]
typecheck:
    uv run {{ pre-commit }} mypy

[group('lint')]
check:
    {{ pre-commit }}

[group('test')]
test:
    uv run pytest tests

[group('test')]
cov:
    uv run pytest --cov=src

[group('test')]
cov-report-markdown:
    uv run python -m coverage report --format=markdown > coverage.md

[group('test')]
@cov-total:
    uv run python -m coverage json --quiet
    uv run python -c "import json;print(json.load(open('coverage.json'))['totals']['percent_covered_display'])"

config := "--config-file=docs/mkdocs.yml"

[group('docs')]
docs-build:
    uv run mkdocs build {{ config }}

[group('docs')]
docs-serve:
    uv run mkdocs serve {{ config }} --verbose

[group('docs')]
docs-deploy:
    uv run mike deploy {{ config }} --push --update-aliases $(just project-version) latest
