import io
import sys

from factorlab.cli import build_parser, configure_logging, run_from_args


def test_configure_logging_levels():
    configure_logging(0)
    configure_logging(1)
    configure_logging(2)


def test_build_parser_has_subcommands():
    p = build_parser()
    help_text = p.format_help()
    assert "calc" in help_text and "validate" in help_text and "bench" in help_text


def test_run_from_args_calc_n_text(capsys):
    code = run_from_args(["calc", "--n", "6"])
    assert code == 0
    out = capsys.readouterr().out
    assert "6! = 720" in out


def test_run_from_args_calc_stdin_invalid(monkeypatch, capsys, caplog):
    import io
    import logging

    caplog.set_level(logging.ERROR, logger="factorlab")
    monkeypatch.setattr(sys, "stdin", io.StringIO("a b c"))
    code = run_from_args(["calc"])
    assert code == 2
    streams = capsys.readouterr()
    err = streams.err
    text = caplog.text
    assert ("inválida" in err or "inválido" in err) or ("inválida" in text or "inválido" in text)


def test_run_from_args_calc_input_missing(capsys, caplog):
    import logging

    caplog.set_level(logging.ERROR, logger="factorlab")
    code = run_from_args(["calc", "--input", "no-existe.txt"])
    assert code == 2
    streams = capsys.readouterr()
    err = streams.err
    text = caplog.text
    assert "No se pudo abrir" in err or "No se pudo abrir" in text


def test_run_from_args_calc_stdin_ok_csv(monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", io.StringIO("3 4"))
    code = run_from_args(["calc", "--format", "csv"])
    assert code == 0
    out = capsys.readouterr().out
    assert "3,6" in out and "4,24" in out


def test_run_from_args_calc_output_file(tmp_path):
    out = tmp_path / "salida.txt"
    code = run_from_args(["calc", "--n", "5", "--output", str(out)])
    assert code == 0
    assert out.read_text(encoding="utf-8").strip().endswith("120")


def test_run_from_args_validate_paths(capsys):
    assert run_from_args(["validate", "--n", "10"]) == 0
    code = run_from_args(["validate", "--n", "-1"])
    assert code == 2


def test_run_from_args_bench_stdout(capsys):
    code = run_from_args(["bench", "--range", "1:5:2", "--method", "math"])
    assert code == 0
    out = capsys.readouterr().out
    assert out.splitlines()[0] == "n,digits,seconds,method"
