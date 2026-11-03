"""Compile the generated VHDL with GHDL against the general-cores used in production.

For every case: analyse <unit>_auto_pkg.vhd, <unit>_auto.vhd and the stub <unit>.vhd,
then elaborate <unit>_auto. Dependencies (genram_pkg, wishbone_pkg, wbgenplus_pkg,
wb_skidpad) come from bel_projects' general-cores submodule.

Skipped if ghdl is not on PATH or bel_projects is missing ($WBGEN_BEL_PROJECTS,
default ../bel_projects).
"""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from helpers import CASES, REPO, all_cases, run_wbgenplus

BEL = Path(os.environ.get("WBGEN_BEL_PROJECTS", REPO.parent / "bel_projects"))
GC = BEL / "ip_cores/general-cores/modules"
DEPS = [
    GC / "genrams/genram_pkg.vhd",
    GC / "wishbone/wishbone_pkg.vhd",
    GC / "wishbone/wbgenplus/wbgenplus_pkg.vhd",
    GC / "wishbone/wb_register/wb_skidpad.vhd",
]
GHDL = shutil.which("ghdl")
FLAGS = ["--std=08", "-frelaxed", "-Wno-hide"]

KNOWN = {
    "complex_demo":      "1.5/1.6: paged registers (r_p/v_p undeclared, mget args swapped, 2D aggregate); 1.2: r_stall undeclared",
    "intermediate_demo": "1.5/1.6: paged registers (r_p/v_p undeclared, mget args swapped, 2D aggregate)",
}

pytestmark = [
    pytest.mark.skipif(GHDL is None, reason="ghdl not found on PATH"),
    pytest.mark.skipif(not GC.is_dir(), reason=f"general-cores not found at {GC}"),
]


def _ghdl(*args, cwd):
    return subprocess.run([GHDL, *args], cwd=cwd, capture_output=True, text=True, timeout=120)


@pytest.fixture(scope="session")
def deps_lib(tmp_path_factory):
    """Analyse general-cores dependencies once; return the work library file."""
    d = tmp_path_factory.mktemp("ghdl_deps")
    for f in DEPS:
        r = _ghdl("-a", *FLAGS, str(f), cwd=d)
        assert r.returncode == 0, f"dependency {f.name} failed:\n{r.stderr}"
    return d / "work-obj08.cf"


def _params():
    for case in all_cases():
        name = Path(case).name
        marks = [pytest.mark.xfail(reason=KNOWN[name], strict=True)] if name in KNOWN else []
        yield pytest.param(case, marks=marks, id=case)


@pytest.mark.parametrize("case", list(_params()))
def test_ghdl_compile(case, tmp_path, deps_lib):
    proc, out = run_wbgenplus(CASES / f"{case}.xml", tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    work = tmp_path / "work"
    shutil.copy(deps_lib, work)
    unit = Path(case).name
    for f in (f"{unit}_auto_pkg.vhd", f"{unit}_auto.vhd", f"{unit}.vhd"):
        r = _ghdl("-a", *FLAGS, f, cwd=work)
        assert r.returncode == 0, f"analysis of {f} failed:\n{r.stderr[-3000:]}"
    r = _ghdl("-e", *FLAGS, f"{unit}_auto", cwd=work)
    assert r.returncode == 0, f"elaboration of {unit}_auto failed:\n{r.stderr[-3000:]}"
