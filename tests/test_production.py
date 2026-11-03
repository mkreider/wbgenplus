"""Compare generator output with the *_auto(_pkg).vhd files committed in bel_projects.

Only date and copyright-year lines are ignored. Known deviations are strict xfails
and reference a finding in REVIEW_STATE.md; once a fix makes the output match,
the xfail fails, and the marker must be removed.

bel_projects is looked up at $WBGEN_BEL_PROJECTS or ../bel_projects; the tests are
skipped if it is missing.
"""
import os
import re
from pathlib import Path

import pytest

from helpers import CASES, REPO, run_wbgenplus

BEL = Path(os.environ.get("WBGEN_BEL_PROJECTS", REPO.parent / "bel_projects"))

PROD_DIRS = {
    "dm_diag": "modules/dm_diag",
    "eca_tap": "modules/eca_tap",
    "oled":    "modules/oled_display",
    "prio":    "modules/prioq2",
}

KNOWN = {
    ("dm_diag", "auto"):     "1.13: word order of multi-word registers (prod is high word first)",
    ("dm_diag", "auto_pkg"): "1.13: word order of multi-word registers (prod is high word first)",
    ("eca_tap", "auto"):     "1.13: word order of multi-word registers (prod is high word first)",
    ("eca_tap", "auto_pkg"): "1.13: word order of multi-word registers (prod is high word first)",
    ("oled",    "auto_pkg"): "1.16: SDB addr_last 0x0f excludes last register at 0x10",
}

_IGNORE = re.compile(r"@date|@copyright|^\s*date\s+=>")


def _norm(text):
    return [l for l in text.splitlines() if not _IGNORE.search(l)]


def _params():
    for unit in PROD_DIRS:
        for kind in ("auto", "auto_pkg"):
            marks = [pytest.mark.xfail(reason=KNOWN[(unit, kind)], strict=True)] if (unit, kind) in KNOWN else []
            yield pytest.param(unit, kind, marks=marks, id=f"{unit}_{kind}")


@pytest.mark.skipif(not BEL.is_dir(), reason=f"bel_projects not found at {BEL}")
@pytest.mark.parametrize("unit,kind", list(_params()))
def test_matches_production(unit, kind, tmp_path):
    proc, out = run_wbgenplus(CASES / "prod" / f"{unit}.xml", tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    name = f"{unit}_{kind}.vhd"
    prod = (BEL / PROD_DIRS[unit] / name).read_text()
    assert _norm(out[name].decode()) == _norm(prod)
