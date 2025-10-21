import pytest

from factorlab.strategies import (
    IterativeStrategy,
    MathProdStrategy,
    RecursiveStrategy,
    get_strategy,
)


def test_get_strategy_valid_names():
    assert isinstance(get_strategy("iter"), IterativeStrategy)
    assert isinstance(get_strategy("iterative"), IterativeStrategy)
    assert isinstance(get_strategy("rec"), RecursiveStrategy)
    assert isinstance(get_strategy("recursive"), RecursiveStrategy)
    assert isinstance(get_strategy("math"), MathProdStrategy)
    assert isinstance(get_strategy("prod"), MathProdStrategy)


def test_get_strategy_invalid_name():
    with pytest.raises(ValueError):
        get_strategy("unknown")
