"""Domain service: validation, selection of strategy, formatting."""

from __future__ import annotations

import time
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from .exceptions import ComputationError, ValidationError
from .strategies import IterativeStrategy, MathProdStrategy, RecursiveStrategy, Strategy

OutputFormat = Literal["text", "json", "csv"]
MethodName = Literal["iterative", "recursive", "math"]
Row = dict[str, float | int | str]


@dataclass(frozen=True)
class Config:
    """Configuration for factorial computation and formatting."""

    max_n: int = 100_000  # configurable guardrail
    method: MethodName = "math"
    output: OutputFormat = "text"


class FactorialService:
    """Application/service layer to compute factorials with validations and formatting."""

    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config()

    def validate_n(self, n: int) -> None:
        """Validate that n is a non-negative integer and within allowed range."""
        if not isinstance(n, int):
            raise ValidationError("n debe ser un entero.")
        if n < 0:
            raise ValidationError("n debe ser >= 0.")
        if n > self.config.max_n:
            raise ValidationError(f"n excede el máximo permitido ({self.config.max_n}).")
        if self.config.method == "recursive" and n > 2000:
            raise ValidationError("La estrategia recursiva no es segura para n > 2000.")

    def _select_strategy(self) -> Strategy:
        name = self.config.method
        if name == "iterative":
            return IterativeStrategy()
        if name == "recursive":
            return RecursiveStrategy()
        return MathProdStrategy()

    def factorial(self, n: int) -> int:
        """Compute factorial for a single n after validation."""
        self.validate_n(n)
        strategy = self._select_strategy()
        try:
            return strategy.compute(n)
        except Exception as exc:  # noqa: BLE001
            raise ComputationError("Fallo durante el cálculo del factorial.") from exc

    def factorial_many(self, values: Sequence[int]) -> list[tuple[int, int]]:
        """Compute factorials for a sequence of n's, validating each one."""
        results: list[tuple[int, int]] = []
        for n in values:
            results.append((n, self.factorial(n)))
        return results

    # --------- formatting helpers ---------
    @staticmethod
    def to_text(pairs: Sequence[tuple[int, int]]) -> str:
        lines = [f"{n}! = {val}" for n, val in pairs]
        return "\n".join(lines)

    @staticmethod
    def to_json(pairs: Sequence[tuple[int, int]]) -> list[dict[str, int | str]]:
        out: list[dict[str, int | str]] = []
        for n, val in pairs:
            out.append({"n": n, "value": str(val), "digits": len(str(val))})
        return out

    @staticmethod
    def to_csv(pairs: Sequence[tuple[int, int]]) -> str:
        rows = ["n,value,digits"]
        for n, val in pairs:
            sval = str(val)
            rows.append(f"{n},{sval},{len(sval)}")
        return "\n".join(rows)

    # --------- benchmarking ---------
    def bench_range(self, start: int, stop: int, step: int = 1) -> list[Row]:
        """Benchmark computation times across a range of n values."""
        data: list[Row] = []
        for n in range(start, stop + 1, step):
            self.validate_n(n)
            t0 = time.perf_counter()
            val = self.factorial(n)
            elapsed = time.perf_counter() - t0
            data.append(
                {"n": n, "digits": len(str(val)), "seconds": elapsed, "method": self.config.method}
            )
        return data
