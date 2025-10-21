from factorlab.exceptions import ComputationError, FactorlabError, ValidationError


def test_exception_hierarchy():
    assert issubclass(ValidationError, FactorlabError)
    assert issubclass(ComputationError, FactorlabError)
