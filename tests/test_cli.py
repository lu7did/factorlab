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


def test_cli_calc_n_text():
    code, out, err = run_cli(["calc", "--n", "5"])
    assert code == 0
    assert "5! = 120" in out


def test_cli_calc_stdin_csv():
    code, out, err = run_cli(["calc", "--format", "csv"], input_text="3 4")
    assert code == 0
    assert "3,6" in out and "4,24" in out


def test_cli_validate():
    code, out, err = run_cli(["validate", "--n", "10"])
    assert code == 0
    assert "OK" in out


def test_cli_bench():
    code, out, err = run_cli(["bench", "--range", "1:10:3", "--method", "math"])
    assert code == 0
    assert out.splitlines()[0] == "n,digits,seconds,method"
