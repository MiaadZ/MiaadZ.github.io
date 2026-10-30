#!/usr/bin/env python3
"""Compatibility entry point: Phase 2's checks now cover the completed migration.
Use docs/verify-writeups.py directly for new workflows.
"""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name("verify-writeups.py")), run_name="__main__")
