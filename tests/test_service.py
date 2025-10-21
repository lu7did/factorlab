import pytest

from factorlab.exceptions import ValidationError
from factorlab.service import Config, FactorialService


def test_validate_ok_and_compute():
    svc = FactorialService(Config(max_n=100, method="math"))
    assert svc.factorial(10) == 3628800


def test_validate_negative():
    svc = FactorialService()
    with pytest.raises(ValidationError):
        svc.validate_n(-1)


def test_validate_exceeds():
    svc = FactorialService(Config(max_n=5))
    with pytest.raises(ValidationError):
        svc.validate_n(10)


def test_many_and_formats():
    svc = FactorialService()
    pairs = svc.factorial_many([3, 4])
    assert pairs[0][1] == 6 and pairs[1][1] == 24
    assert "3! = 6" in svc.to_text(pairs)
    js = svc.to_json(pairs)
    assert js[0]["n"] == 3 and isinstance(js[1]["value"], str)
    csv = svc.to_csv(pairs)
    assert "n,value,digits" in csv
