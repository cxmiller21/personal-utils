import os
import subprocess
from pathlib import Path


def run_test():
    """Run unittests"""
    # Ensure we're running from the python3 directory
    script_dir = Path(__file__).parent
    subprocess.run(["pytest", "cm_util/tests/"], cwd=script_dir, check=True, timeout=300)


def run_coverage():
    """Run coverage"""
    # Ensure we're running from the python3 directory
    script_dir = Path(__file__).parent
    subprocess.run(
        ["python", "-m", "coverage", "run", "-m", "pytest", "cm_util/tests/"],
        cwd=script_dir,
        check=True,
        timeout=300,
    )
    subprocess.run(
        ["python", "-m", "coverage", "report", "-m"],
        cwd=script_dir,
        check=True,
        timeout=60,
    )
    subprocess.run(["python", "-m", "coverage", "html"], cwd=script_dir, check=True, timeout=60)
