pip install -r requirements-dev.txt
make security            # ahora usa .bandit (YAML) y no debería fallar con B110
make ci-lint             # ruff/black/mypy/bandit
make test

