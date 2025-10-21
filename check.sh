pip install -r requirements-dev.txt

make security   # usa .bandit, cae a flags si hiciera falta
make ci-lint    # ruff/format-check + black_safe + mypy + bandit
make test

