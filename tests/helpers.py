"""Shared helpers for running wbgenplus in an isolated directory."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CASES = Path(__file__).resolve().parent / "cases"
GOLDEN = Path(__file__).resolve().parent / "golden"

# Fixed generation date for reproducible output: 2023-11-14 22:13:20 UTC
SOURCE_DATE_EPOCH = "1700000000"


def all_cases():
    """Return case names relative to CASES, without .xml (e.g. 'simple_demo', 'prod/oled')."""
    return sorted(str(p.relative_to(CASES).with_suffix("")) for p in CASES.rglob("*.xml"))


def run_wbgenplus(xml: Path, tmp_path: Path, args=()):
    """Run wbgenplus on a copy of `xml` inside tmp_path/work/.

    The generator is invoked with a bare filename (cwd = work dir), so finding 1.7
    (missing path separator) does not affect where files land. Any file written
    outside work/ is still collected so stray output is detected.

    Returns (CompletedProcess, {relative_path: bytes}) for every file except the input.
    """
    work = tmp_path / "work"
    work.mkdir(parents=True)
    shutil.copy(xml, work / xml.name)
    env = dict(os.environ, SOURCE_DATE_EPOCH=SOURCE_DATE_EPOCH, PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, str(REPO / "wbgenplus.py"), xml.name, *args],
        cwd=work, env=env, capture_output=True, text=True, timeout=60,
    )
    out = {}
    for p in tmp_path.rglob("*"):
        if p.is_file() and p != work / xml.name:
            out[str(p.relative_to(work)) if p.is_relative_to(work) else "../" + str(p.relative_to(tmp_path))] = p.read_bytes()
    return proc, out
