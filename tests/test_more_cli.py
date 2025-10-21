import json
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


def test_cli_calc_requires_input_when_no_stdin(tmp_path):
    code, out, err = run_cli(["calc"])
    assert code == 2  # argparse error


def test_cli_input_file_invalid(tmp_path):
    p = tmp_path / "nums.txt"
    p.write_text("1\n2\nX\n", encoding="utf-8")
    code, out, err = run_cli(["calc", "--input", str(p)])
    assert code == 2
    assert "inválido" in err or "invalido" in err.lower()


def test_cli_output_file_write_error(tmp_path):
    # Use a directory path as output to force write failure
    bad_out = tmp_path / "outdir"
    bad_out.mkdir()
    code, out, err = run_cli(["calc", "--n", "4", "--output", str(bad_out)])
    assert code == 2


def test_cli_stdin_numbers():
    code, out, err = run_cli(["calc", "--format", "csv"], input_text="3 4 5")
    assert code == 0
    assert "3,6" in out and "4,24" in out and "5,120" in out


def test_cli_calc_json_to_file(tmp_path):
    p = tmp_path / "nums.txt"
    p.write_text("3\n4\n", encoding="utf-8")
    outp = tmp_path / "res.json"
    code, out, err = run_cli(["calc", "--input", str(p), "--format", "json", "--output", str(outp)])
    assert code == 0
    data = json.loads(outp.read_text(encoding="utf-8"))
    assert isinstance(data, list) and data[0]["n"] == 3


def test_cli_bench_to_file(tmp_path):
    outp = tmp_path / "bench.csv"
    code, out, err = run_cli(["bench", "--range", "1:5:2", "--output", str(outp)])
    assert code == 0
    txt = outp.read_text(encoding="utf-8")
    assert txt.splitlines()[0] == "n,digits,seconds,method"


def test_cli_validate_ok():
    code, out, err = run_cli(["validate", "--n", "10"])
    assert code == 0 and "OK" in out
