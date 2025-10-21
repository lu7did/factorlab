import subprocess
import sys


def test_main_help_runs():
    # Call with --help to ensure __main__ path is executed without heavy work
    proc = subprocess.run(
        [sys.executable, "-m", "factorlab", "--help"], capture_output=True, check=False
    )
    assert proc.returncode == 0
    assert b"factorlab" in proc.stdout
