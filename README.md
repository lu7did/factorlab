# factorlab

**factorlab** calcula factoriales con buenas prácticas de ingeniería:

- Python ≥ 3.12, layout `src/` (estilo cookiecutter).
- OOP + patrones: Strategy (método de cálculo), Factory + servicio con validaciones.
- PEP8/PEP257, Black + Ruff, tipado estricto con MyPy.
- PyTest con cobertura objetivo cercano al 80%+.
- Bandit para chequeos de seguridad.
- Empaquetado como `factorlab` con script `factorlab`.

![CI](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml?branch=main)
![Coverage](https://img.shields.io/badge/coverage-codecov-blue)
![PyPI](https://img.shields.io/pypi/v/factorlab.svg)

## Instalación (dev)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements-dev.txt
pip install -e .
```

## Uso rápido

```bash
# 1) CLI simple
factorlab calc --n 10
# -> 10! = 3628800

# 2) Múltiples n por archivo a CSV
echo -e "3\n4\n5" > ns.txt
factorlab calc --input ns.txt --format csv --output out.csv

# 3) Validación
factorlab validate --n 50000

# 4) Benchmark a CSV
factorlab bench --range 1:1000:100 --method math --output bench.csv
```

## CI/CD
Este repo incluye:
- **GitHub Actions** para *lint*, *type-check*, *tests* y *coverage* (`.github/workflows/ci.yml`).
- **Publicación** a TestPyPI/PyPI por tags (`publish.yml`) con secrets: `TEST_PYPI_API_TOKEN` y `PYPI_API_TOKEN`.
- **Docs** con **pdoc** y despliegue a GitHub Pages (`docs.yml`).

### Codecov
1. Crear proyecto en codecov.io
2. Añadir `CODECOV_TOKEN` en *Settings → Secrets → Actions* del repo.
3. La CI sube `coverage.xml` y actualiza el badge.

### GitHub Pages
- Activar en *Settings → Pages* la rama `gh-pages`. Los cambios en `main` regeneran docs.

## Comandos útiles (local)
```bash
make format
make lint
make type
make test
make security
make docs
make ci-lint
```


> Nota: Bandit ahora usa configuración YAML en `.bandit` (antes `bandit.ini`).
