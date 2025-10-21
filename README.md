# factorlab

**factorlab** calcula factoriales con buenas prácticas de ingeniería:

- Python ≥ 3.12, layout `src/` (estilo cookiecutter).
- OOP + patrones: `Strategy` (método de cálculo), `Factory` para seleccionar estrategia, y un **servicio** que aplica validaciones (separación dominio/CLI).
- PEP8/PEP257, Black + Ruff, tipado estricto con MyPy.
- PyTest con cobertura objetivo ≥ 80%.
- Bandit para chequeos de seguridad.
- Empaquetado como `factorlab` con script `factorlab`.

## Uso rápido

```bash
# Cálculo simple del factorial de 10
factorlab calc --n 10

# Leer múltiples n desde archivo y emitir CSV
factorlab calc --input ns.txt --format csv --output out.csv

# Validación de un n (rango/tipo)
factorlab validate --n 50000

# Benchmark (resultados en CSV)
factorlab bench --range 1:1000:100 --output bench.csv
```

## Formatos
- `text` (por defecto): `n! = <valor>`
- `json`: una lista de objetos `{ "n": int, "value": str, "digits": int }`
- `csv`: columnas `n,value,digits`

## Calidad
- `make all` ejecuta formateo, lint, tipos, tests y seguridad.


## Nota sobre Python 3.12.5 y Black

Si ves el aviso **"Python 3.12.5 has a memory safety issue that can cause Black's AST safety checks to fail"**, el proyecto ya está configurado para evitarlo sin cambiar de versión de Python:

- El `Makefile` ejecuta **Black con `--fast`**, lo que desactiva el chequeo de equivalencia del AST (la parte afectada) y deja el formateo principal a cargo de **Ruff**.
- Si usas *pre-commit*, el hook de Black también corre con `--fast`.

Comandos útiles:
```bash
make format    # ruff format + black --fast
make lint      # ruff check + black --check --diff --fast
pre-commit install -f --install-hooks
```


### Nota sobre `make lint`
El objetivo es **no fallar** por diferencias de formato en 3.12.5. Por eso:
- `ruff check --fix` aplica correcciones seguras.
- `ruff format` normaliza el estilo.
- Se ejecuta el wrapper `black_safe` (API) y luego `black --check --diff --fast`, pero este último **no corta** el build (`|| true`).

Si querés que falle ante cualquier diferencia, quitá `|| true` del Makefile.
