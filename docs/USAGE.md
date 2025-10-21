# Guía de uso

## Subcomandos
- `calc`: calcula factorial(es) desde `--n`, `--input` o `stdin`.
- `validate`: valida un `n` sin calcular.
- `bench`: mide tiempos de cálculo para un rango de `n`.

## Ejemplos
```bash
factorlab calc --n 5
factorlab calc --input numeros.txt --format json --output salida.json
echo "3 4 5" | factorlab calc --format csv
factorlab validate --n 1000
factorlab bench --range 1:1000:100 --method math --output bench.csv
```
