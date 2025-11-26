import subprocess


def run_test():
    """Run unittests"""
    subprocess.run(["pytest", "cm_util/tests/"])


def run_coverage():
    """Run coverage"""
    subprocess.run(["coverage", "run", "-m", "pytest", "cm_util/tests/"])
    subprocess.run(["coverage", "report", "-m"])
    subprocess.run(["coverage", "html"])
