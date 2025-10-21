import pytest

from factorlab.strategies import (
    IterativeStrategy,
    MathProdStrategy,
    RecursiveStrategy,
    get_strategy,
)


def test_iterative_small():
    assert IterativeStrategy().compute(5) == 120


def test_recursive_small():
    assert RecursiveStrategy().compute(0) == 1
    assert RecursiveStrategy().compute(3) == 6


def test_mathprod_small():
    assert MathProdStrategy().compute(1) == 1
    assert MathProdStrategy().compute(6) == 720


def test_get_strategy_aliases():
    assert isinstance(get_strategy("iter"), IterativeStrategy)
    assert isinstance(get_strategy("iterative"), IterativeStrategy)
    assert isinstance(get_strategy("rec"), RecursiveStrategy)
    assert isinstance(get_strategy("recursive"), RecursiveStrategy)
    assert isinstance(get_strategy("math"), MathProdStrategy)
    assert isinstance(get_strategy("prod"), MathProdStrategy)


def test_get_strategy_invalid():
    with pytest.raises(ValueError):
        get_strategy("nope")
