import pytest

from factorlab.exceptions import ValidationError
from factorlab.service import Config, FactorialService


def test_strategy_selection_iterative():
    svc = FactorialService(Config(method="iterative"))
    assert svc.factorial(5) == 120


def test_strategy_selection_recursive():
    svc = FactorialService(Config(method="recursive"))
    assert svc.factorial(5) == 120


def test_strategy_selection_math():
    svc = FactorialService(Config(method="math"))
    assert svc.factorial(6) == 720


def test_validate_non_int_type():
    svc = FactorialService()
    with pytest.raises(ValidationError):
        svc.validate_n(3.14)  # type: ignore[arg-type]


def test_validate_max_n_guard():
    svc = FactorialService(Config(max_n=3))
    with pytest.raises(ValidationError):
        svc.factorial(10)


def test_factorial_many_and_formats_details():
    svc = FactorialService()
    pairs = svc.factorial_many([0, 1, 5])
    txt = svc.to_text(pairs)
    js = svc.to_json(pairs)
    csv = svc.to_csv(pairs)
    assert "0! = 1" in txt and "5! = 120" in txt
    assert js[2]["n"] == 5 and js[2]["value"] == "120" and js[2]["digits"] == 3
    assert "n,value,digits" in csv and "5,120,3" in csv
