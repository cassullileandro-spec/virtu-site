"""Rebuild all 16 approved Figma pages."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("sync-figma.py")), run_name="__main__")
