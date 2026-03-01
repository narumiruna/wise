# Repository Guidelines

## Project Structure & Module Organization
Core package code lives in `src/wise/` (`cli.py`, `rate.py`, `price.py`, `currency.py`, `cost.py`, `method.py`). Keep domain logic in these modules and keep CLI wiring in `cli.py`.  
Tests live in `tests/` and follow one-file-per-domain patterns such as `test_rate.py` and `test_currency.py`.  
Utility and exploratory scripts live in `scripts/` (for example, `rate_history.py` and `available_currencies.py`).

## Build, Test, and Development Commands
Use `uv` for all local workflows.

- `uv sync --dev`: install runtime + dev dependencies.
- `make format`: run `ruff format`.
- `make lint`: run `ruff check`.
- `make type`: run `ty check`.
- `make test`: run `pytest -v -s --cov=src tests`.
- `make all`: run format, lint, type, and tests in sequence.
- `uv run wise GBP 1000 USD`: run the CLI locally.

If `.pre-commit-config.yaml` is present, run `prek run -a` before opening a PR.

## Coding Style & Naming Conventions
Target Python 3.11+ with explicit type hints. Follow Ruff defaults with max line length `120`.  
Use `snake_case` for functions/modules/variables, `PascalCase` for classes, and clear domain names (`rate`, `price`, `currency`).  
Keep imports tidy and deterministic (Ruff isort rules enforce single-line imports).  
Prefer small, focused functions over cross-module abstractions.

## Testing Guidelines
Use `pytest` with `pytest-cov`. Place tests under `tests/` and name files `test_*.py`; test functions should be `test_*`.  
Add or update tests for any behavior change, especially CLI parsing and conversion logic.  
Run `make test` locally and ensure coverage still includes modified paths in `src/`.

## Commit & Pull Request Guidelines
Match repository history: short, imperative commit subjects (for example, `add tombi pre-commit hook`, `rename package`).  
Use optional conventional prefixes when appropriate (for example, `build(deps): ...`).  
For PRs, include:

- A concise summary of behavior changes.
- Linked issue(s) when applicable.
- Test evidence (command + result, e.g., `make all`).
- CLI output examples when user-facing behavior changes.
