import pytest

from factorlab.exceptions import ComputationError, ValidationError
from factorlab.service import Config, FactorialService


def test_recursive_limit():
    svc = FactorialService(Config(method="recursive"))
    with pytest.raises(ValidationError):
        svc.validate_n(3000)


def test_computation_wrapped_error(monkeypatch):
    svc = FactorialService()

    class Boom:
        def compute(self, n: int) -> int:  # type: ignore[override]
            raise ValueError("boom")

    monkeypatch.setattr(svc, "_select_strategy", lambda: Boom())
    with pytest.raises(ComputationError):
        svc.factorial(3)


def test_bench_range_small():
    svc = FactorialService(Config(method="math"))
    data = svc.bench_range(1, 5, 2)
    assert len(data) == 3
    assert set(data[0].keys()) == {"n", "digits", "seconds", "method"}


def test_format_helpers():
    svc = FactorialService()
    pairs = [(5, 120)]
    assert "5! = 120" in svc.to_text(pairs)
    js = svc.to_json(pairs)
    assert js[0]["n"] == 5 and js[0]["digits"] == len(str(120))
    csv = svc.to_csv(pairs)
    assert "n,value,digits" in csv and "5,120,3" in csv
