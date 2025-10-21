import io
import sys

import pytest

from factorlab.cli import run_from_args


def test_validate_error_message(capsys):
    code = run_from_args(["validate", "--n", "-5"])
    assert code == 2
    out = capsys.readouterr()
    assert "debe ser >=" in (out.err + out.out)


def test_calc_missing_all_inputs(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    with pytest.raises(SystemExit):
        run_from_args(["calc"])
