import subprocess


def run_test():
    """Run unittests"""
    subprocess.run(["poetry", "run", "pytest", "tests/"])


def run_coverage():
    """Run coverage"""
    # omit="--omit='tests/*'"
    omit = ""
    subprocess.run(["coverage", "run", "-m", "pytest"])
    subprocess.run(["coverage", "report", "-m"])
    subprocess.run(["coverage", "html"])
