"""Factorial strategies (Strategy pattern) and a simple factory."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol


class Strategy(Protocol):
    """Interface for factorial strategies."""

    def compute(self, n: int) -> int:
        """Compute n! and return it."""


@dataclass(frozen=True)
class IterativeStrategy:
    """Iterative factorial using a simple loop."""

    def compute(self, n: int) -> int:
        result = 1
        for k in range(2, n + 1):
            result *= k
        return result


@dataclass(frozen=True)
class RecursiveStrategy:
    """Recursive factorial (educational; avoid for very large n)."""

    def compute(self, n: int) -> int:
        if n < 2:
            return 1
        return n * self.compute(n - 1)


@dataclass(frozen=True)
class MathProdStrategy:
    """Factorial via math.prod for readability/performance."""

    def compute(self, n: int) -> int:
        return math.prod(range(2, n + 1)) if n > 1 else 1


def get_strategy(name: str) -> Strategy:
    """Factory that returns a strategy instance by name."""
    key = name.lower()
    if key in {"iter", "iterative"}:
        return IterativeStrategy()
    if key in {"rec", "recursive"}:
        return RecursiveStrategy()
    if key in {"prod", "math", "mathprod"}:
        return MathProdStrategy()
    raise ValueError(f"Estrategia desconocida: {name}")
