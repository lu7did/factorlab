.PHONY: format lint type test security all clean build docs ci-lint hooks

format:
	ruff format . || ruff check --fix .
	PYTHONPATH=src python -m factorlab.tools.black_safe .

lint:
	ruff check --fix .
	ruff format .
	ruff check --exit-zero .
	PYTHONPATH=src python -m factorlab.tools.black_safe .
	PYTHONPATH=src python -m factorlab.tools.black_safe . && black --check --diff --fast . || true || true

type:
	mypy src

test:
	pytest

security:
	bandit -c .bandit -r src/factorlab || bandit -r src/factorlab -x tests -s B101,B110

docs:
	pdoc -o docs src/factorlab

ci-lint:
	ruff check .
	ruff format --check .
	PYTHONPATH=src python -m factorlab.tools.black_safe . && black --check --diff --fast . || true
	mypy src
	bandit -c .bandit -r src/factorlab || bandit -r src/factorlab -x tests -s B101,B110 -q

all: format lint type test security

build:
	python -m build

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage dist build *.egg-info site htmlcov
