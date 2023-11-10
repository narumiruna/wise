install:
	poetry install

lint:
	poetry run flake8 -v .

test:
	poetry run pytest -v -s --cov=wise tests

.PHONY: lint test cover
