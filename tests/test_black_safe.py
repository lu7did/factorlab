import subprocess
import sys


def test_black_safe_runs_on_temp_dir(tmp_path):
    py = tmp_path / "t.py"
    py.write_text("x=1\n", encoding="utf-8")
    env = {**dict(), "PYTHONPATH": "src"}
    proc = subprocess.run(
        [sys.executable, "-m", "factorlab.tools.black_safe", str(tmp_path)],
        capture_output=True,
        check=False,
        env=env,
    )
    # Expect success (0) or warning-only; wrapper returns 0 even on internal warnings
    assert proc.returncode == 0
