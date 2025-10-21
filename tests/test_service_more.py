import pytest

from factorlab.exceptions import ComputationError, ValidationError
from factorlab.service import Config, FactorialService


def test_recursive_limit_validation():
    svc = FactorialService(Config(method="recursive"))
    with pytest.raises(ValidationError):
        svc.validate_n(50000)


def test_bench_range_shape():
    svc = FactorialService(Config(method="math", max_n=2000))
    data = svc.bench_range(1, 10, 3)
    assert len(data) == 4
    assert {"n", "digits", "seconds", "method"}.issubset(set(data[0].keys()))


def test_computation_error(monkeypatch):
    svc = FactorialService()

    class BadStrategy:
        def compute(self, n: int):
            raise RuntimeError("boom")

    monkeypatch.setattr(svc, "_select_strategy", lambda: BadStrategy())
    with pytest.raises(ComputationError):
        svc.factorial(3)
