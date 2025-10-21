"""factorlab package initialization."""

from .exceptions import ComputationError, FactorlabError, ValidationError
from .service import Config, FactorialService
from .strategies import IterativeStrategy, MathProdStrategy, RecursiveStrategy, Strategy

__all__ = [
    "FactorialService",
    "Config",
    "Strategy",
    "IterativeStrategy",
    "RecursiveStrategy",
    "MathProdStrategy",
    "FactorlabError",
    "ValidationError",
    "ComputationError",
]
