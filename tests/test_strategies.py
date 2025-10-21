from factorlab.strategies import IterativeStrategy, MathProdStrategy, RecursiveStrategy


def test_iterative_small():
    assert IterativeStrategy().compute(5) == 120


def test_recursive_small():
    assert RecursiveStrategy().compute(0) == 1
    assert RecursiveStrategy().compute(3) == 6


def test_mathprod_small():
    assert MathProdStrategy().compute(1) == 1
    assert MathProdStrategy().compute(6) == 720
