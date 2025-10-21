import subprocess
import sys

PY = sys.executable


def run_cli(args, input_text=""):
    proc = subprocess.run(
        [PY, "-m", "factorlab"] + args,
        input=input_text.encode(),
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout.decode(), proc.stderr.decode()


def test_cli_calc_requires_input(capsys, caplog):
    import logging

    caplog.set_level(logging.ERROR, logger="factorlab")
    code, out, err = run_cli(["calc"])
    # argparse error triggers SystemExit before our code; allow non-zero return
    if code == 0:
        assert "Debes especificar" in out + err or "Debes especificar" in caplog.text


def test_cli_calc_input_file_invalid(tmp_path, caplog):
    import logging

    caplog.set_level(logging.ERROR, logger="factorlab")
    p = tmp_path / "nums.txt"
    p.write_text("1\nX\n3\n", encoding="utf-8")
    code, out, err = run_cli(["calc", "--input", str(p)])
    assert code == 2
    assert ("inválido" in err or "inválida" in err) or ("inválido" in caplog.text)


def test_cli_output_write_error(tmp_path):
    d = tmp_path / "outdir"
    d.mkdir()
    code, out, err = run_cli(["calc", "--n", "5", "--output", str(d)])
    assert code == 2


def test_cli_json_and_csv_formats(tmp_path):
    infile = tmp_path / "in.txt"
    infile.write_text("3\n4\n", encoding="utf-8")
    code, out, err = run_cli(["calc", "--input", str(infile), "--format", "json"])
    assert code == 0
    assert '"n": 3' in out and '"value": "6"' in out
    code, out, err = run_cli(["calc", "--input", str(infile), "--format", "csv"])
    assert code == 0
    assert "n,value,digits" in out and "4,24" in out


def test_cli_recursive_large_n_validation(caplog):
    import logging

    caplog.set_level(logging.ERROR, logger="factorlab")
    code, out, err = run_cli(["calc", "--n", "3000", "--method", "recursive"])
    assert code == 2
