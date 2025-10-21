"""Command-line interface: user interaction and I/O separated from domain logic."""

from __future__ import annotations

import argparse
import json
import logging
import sys

from .exceptions import FactorlabError
from .service import Config, FactorialService

LOG = logging.getLogger("factorlab")


def _err(message: str, bucket: list[str] | None = None) -> None:
    """Emit a message to stderr and log it as error (always flushed)."""
    if bucket is not None:
        bucket.append(message)
    try:
        sys.stderr.write(message + "\n")
        sys.stderr.flush()
    except Exception:  # pragma: no cover
        pass
    print(message, file=sys.stderr, flush=True)
    LOG.error(message)


def configure_logging(verbosity: int) -> None:
    """Configure a basic console logger based on verbosity level."""
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI with subcommands and options."""
    parser = argparse.ArgumentParser(
        prog="factorlab",
        description="Cálculo de factorial con OOP (Strategy/Factory) y CLI separada.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Aumenta verbosidad.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # calc
    p_calc = sub.add_parser("calc", help="Calcula factorial(es).")
    p_calc.add_argument("--n", type=int, help="Valor n único.")
    p_calc.add_argument("--input", help="Archivo con valores n (uno por línea).")
    p_calc.add_argument("--output", help="Archivo de salida (si no, stdout).")
    p_calc.add_argument(
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Formato de salida.",
    )
    p_calc.add_argument(
        "--method",
        choices=["iterative", "recursive", "math"],
        default="math",
        help="Estrategia de cálculo.",
    )
    p_calc.add_argument(
        "--max-n",
        type=int,
        default=100_000,
        help="Máximo n permitido (guardrail).",
    )

    # validate
    p_val = sub.add_parser("validate", help="Valida un n sin calcular.")
    p_val.add_argument("--n", type=int, required=True)
    p_val.add_argument("--max-n", type=int, default=100_000)

    # bench
    p_bench = sub.add_parser("bench", help="Benchmark de factorial para un rango.")
    p_bench.add_argument("--range", required=True, help="Rango start:stop[:step]")
    p_bench.add_argument(
        "--method",
        choices=["iterative", "recursive", "math"],
        default="math",
    )
    p_bench.add_argument("--max-n", type=int, default=100_000)
    p_bench.add_argument("--output", help="Archivo CSV de salida.")

    return parser


def run_from_args(argv: list[str]) -> int:
    """Run CLI from argv. Returns process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args.verbose)

    errors: list[str] = []
    rc = 0

    try:
        if args.cmd == "calc":
            cfg = Config(max_n=args.max_n, method=args.method, output=args.format)
            svc = FactorialService(cfg)

            # Gather inputs
            values: list[int] = []
            if args.n is not None:
                values.append(args.n)
            if args.input:
                try:
                    with open(args.input, encoding="utf-8") as fh:
                        for line in fh:
                            line = line.strip()
                            if not line:
                                continue
                            values.append(int(line))
                except OSError:
                    _err(f"No se pudo abrir el archivo de entrada: {args.input}", errors)
                    rc = 2
                except ValueError:
                    _err("Archivo de entrada inválido: cada línea debe ser un entero.", errors)
                    rc = 2

            if rc == 0 and not values:
                # Try reading from stdin if piped
                data = sys.stdin.read()
                if data.strip():
                    try:
                        values = [int(x) for x in data.split()]
                    except ValueError:
                        _err("Entrada por stdin inválida: se esperaban enteros.", errors)
                        rc = 2

            if rc == 0 and not values:
                parser.error("Debes especificar --n, --input o stdin.")

            if rc == 0:
                pairs = svc.factorial_many(values)
                if args.format == "text":
                    payload = svc.to_text(pairs)
                elif args.format == "json":
                    payload = json.dumps(svc.to_json(pairs), ensure_ascii=False, indent=2)
                else:
                    payload = svc.to_csv(pairs)

                if args.output:
                    try:
                        with open(args.output, "w", encoding="utf-8") as fh:
                            fh.write(payload)
                    except OSError:
                        _err(f"No se pudo escribir el archivo de salida: {args.output}", errors)
                        rc = 2
                else:
                    sys.stdout.write(payload)

        elif args.cmd == "validate":
            svc = FactorialService(Config(max_n=args.max_n))
            try:
                svc.validate_n(args.n)
            except FactorlabError as exc:
                _err(str(exc), errors)
                rc = 2
            else:
                print("OK")

        elif args.cmd == "bench":
            parts = [int(p) for p in args.range.split(":")]
            if len(parts) not in (2, 3):
                parser.error("--range debe tener el formato start:stop[:step]")
            start, stop = parts[0], parts[1]
            step = parts[2] if len(parts) == 3 else 1
            svc = FactorialService(Config(max_n=args.max_n, method=args.method))
            data = svc.bench_range(start, stop, step)
            # CSV only
            rows = ["n,digits,seconds,method"]
            for row in data:
                rows.append(f"{row['n']},{row['digits']},{row['seconds']},{row['method']}")
            payload = "\n".join(rows)
            if args.output:
                try:
                    with open(args.output, "w", encoding="utf-8") as fh:
                        fh.write(payload)
                except OSError:
                    _err(f"No se pudo escribir el archivo de salida: {args.output}", errors)
                    rc = 2
            else:
                sys.stdout.write(payload)

        else:
            parser.error("Comando desconocido.")

    except FactorlabError as exc:
        _err(str(exc), errors)
        rc = 2
    except Exception:
        LOG.exception("Fallo inesperado")
        rc = 1

    if rc != 0 and errors:
        joined = " | ".join(errors)
        try:
            sys.stderr.write(joined + "\n")
            sys.stderr.flush()
        except Exception:  # pragma: no cover
            pass
        print(joined, file=sys.stderr, flush=True)

    return rc


def main() -> None:
    """Console script entry point."""
    raise SystemExit(run_from_args(sys.argv[1:]))
