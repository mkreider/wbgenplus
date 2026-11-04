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


def run_wbgenplus(xml: Path, tmp_path: Path, args=(), invoke="bare"):
    """Run wbgenplus on a copy of `xml` inside tmp_path/work/.

    invoke selects how the XML is passed:
      "bare"     - cwd = work/, argument "<name>.xml"
      "relative" - cwd = tmp_path, argument "work/<name>.xml"
      "absolute" - cwd = tmp_path/elsewhere/, argument is the absolute path
    Output must land in work/ in every mode. Any file written outside work/ is
    collected with a "../" prefix so stray output is detected.

    Returns (CompletedProcess, {relative_path: bytes}) for every file except the input.
    """
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    shutil.copy(xml, work / xml.name)
    env = dict(os.environ, SOURCE_DATE_EPOCH=SOURCE_DATE_EPOCH, PYTHONDONTWRITEBYTECODE="1")
    if invoke == "bare":
        cwd, arg = work, xml.name
    elif invoke == "relative":
        cwd, arg = tmp_path, f"work/{xml.name}"
    elif invoke == "absolute":
        cwd, arg = tmp_path / "elsewhere", str(work / xml.name)
        cwd.mkdir()
    else:
        raise ValueError(invoke)
    proc = subprocess.run(
        [sys.executable, str(REPO / "wbgenplus.py"), arg, *args],
        cwd=cwd, env=env, capture_output=True, text=True, timeout=60,
    )
    out = {}
    for p in tmp_path.rglob("*"):
        if p.is_file() and p != work / xml.name:
            out[str(p.relative_to(work)) if p.is_relative_to(work) else "../" + str(p.relative_to(tmp_path))] = p.read_bytes()
    return proc, out
