#!/usr/bin/env python3
"""
Simple script to list all e2e tests without running them.

Usage:
    poetry run python tests/e2e/list_tests.py
    poetry run python tests/e2e/list_tests.py --verbose
"""

import subprocess
import sys
from pathlib import Path

def list_tests(verbose: bool = False) -> None:
    """List all e2e tests."""
    root_dir = Path(__file__).parent.parent.parent
    
    cmd = ["poetry", "run", "pytest", "tests/e2e/", "--collect-only"]
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    result = subprocess.run(
        cmd,
        cwd=root_dir,
        capture_output=True,
        text=True,
    )
    
    if result.returncode == 0:
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    else:
        print("Error collecting tests:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    list_tests(verbose=verbose)
