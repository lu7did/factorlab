.PHONY: format lint type test security all clean build hooks

format:
	ruff format . || ruff check --fix .
	PYTHONPATH=src python -m factorlab.tools.black_safe .

lint:
	ruff check --fix .
	ruff format .
	ruff check --exit-zero .
	PYTHONPATH=src python -m factorlab.tools.black_safe .
	black --check --diff --fast . || true

type:
	mypy src

test:
	pytest

security:
	bandit -c bandit.ini -r src/factorlab

hooks:
	pre-commit install -f --install-hooks

all: format lint type test security

build:
	python -m build

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage dist build *.egg-info
