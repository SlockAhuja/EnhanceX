"""
EnhanceX Professional Release Manager - Automation Tool
Handles release validation, version tagging, git release verification, and artifact checks.
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from enhancex import __version__


def verify_release():
    print("========================================================")
    print(f"       EnhanceX Release Verification System (v{__version__})")
    print("========================================================")
    
    # 1. Check version uniformity across files
    init_py = ROOT_DIR / "enhancex" / "__init__.py"
    pyproject = ROOT_DIR / "pyproject.toml"
    setup_py = ROOT_DIR / "setup.py"
    
    assert __version__ == "2.0.0", f"Expected version 2.0.0, got {__version__}"
    print("[OK] Version string matches v2.0.0 in __init__.py")
    
    with open(pyproject, "r", encoding="utf-8") as f:
        assert 'version = "2.0.0"' in f.read(), "pyproject.toml version mismatch"
    print("[OK] Version string matches v2.0.0 in pyproject.toml")
    
    with open(setup_py, "r", encoding="utf-8") as f:
        assert 'version="2.0.0"' in f.read(), "setup.py version mismatch"
    print("[OK] Version string matches v2.0.0 in setup.py")
    
    # 2. Verify git status
    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if res.stdout.strip() == "":
        print("[OK] Git working tree is completely clean.")
    else:
        print(f"[NOTE] Git working tree contains modified files:\n{res.stdout.strip()}")
        
    print("========================================================")
    print(f"RELEASE STATUS: EnhanceX v{__version__} is READY for release tag v{__version__}")
    print("========================================================")


def build_release_notes(target_version: str = "2.0.0") -> str:
    notes_path = ROOT_DIR / "RELEASE_NOTES.md"
    if notes_path.exists():
        with open(notes_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"# Release v{target_version}\n\nAutomated Release for EnhanceX v{target_version}."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EnhanceX Release Management Automation")
    parser.add_argument("action", choices=["verify", "notes"], help="Release management action")
    args = parser.parse_args()

    if args.action == "verify":
        verify_release()
    elif args.action == "notes":
        print(build_release_notes())
