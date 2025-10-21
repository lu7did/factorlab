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


def test_cli_calc_from_stdin_success_csv():
    code, out, err = run_cli(["calc", "--format", "csv"], input_text="3 5")
    assert code == 0
    assert "3,6" in out and "5,120" in out


def test_cli_calc_output_file_success(tmp_path):
    outfile = tmp_path / "out.txt"
    code, out, err = run_cli(["calc", "--n", "7", "--output", str(outfile)])
    assert code == 0
    assert outfile.read_text(encoding="utf-8").strip().endswith("5040")


def test_cli_validate_negative_error():
    code, out, err = run_cli(["validate", "--n", "-1"])
    assert code == 2
    assert "n debe ser >=" in (out + err)


def test_cli_bench_stdout_csv():
    code, out, err = run_cli(["bench", "--range", "1:5:2", "--method", "math"])
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert code == 0
    assert lines[0] == "n,digits,seconds,method"
    assert any(",math" in ln for ln in lines[1:])
