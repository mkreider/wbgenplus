"""Golden-file tests: generator output must match tests/golden/<case>/ byte for byte.

The golden files capture the *current* behaviour, known bugs included. A change that
alters output on purpose must update them deliberately:

    WBGEN_UPDATE_GOLDEN=1 pytest tests/test_golden.py

and the resulting diff of tests/golden/ belongs in the same commit.
"""
import os
import shutil

import pytest

from helpers import CASES, GOLDEN, all_cases, run_wbgenplus

UPDATE = os.environ.get("WBGEN_UPDATE_GOLDEN") == "1"


@pytest.mark.parametrize("case", all_cases())
def test_golden(case, tmp_path):
    proc, out = run_wbgenplus(CASES / f"{case}.xml", tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert out, "no output files generated"
    assert not [k for k in out if k.startswith("../")], f"files written outside output dir: {list(out)}"

    gdir = GOLDEN / case
    if UPDATE:
        shutil.rmtree(gdir, ignore_errors=True)
        gdir.mkdir(parents=True)
        for name, data in out.items():
            (gdir / name).write_bytes(data)
        return

    assert gdir.is_dir(), f"no golden files for {case}; run with WBGEN_UPDATE_GOLDEN=1"
    expected = {p.name: p.read_bytes() for p in gdir.iterdir() if p.is_file()}
    assert sorted(out) == sorted(expected), "set of generated files differs"
    for name in sorted(expected):
        assert out[name].decode() == expected[name].decode(), f"{case}/{name} differs from golden"
