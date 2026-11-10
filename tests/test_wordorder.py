"""Finding 1.13: the word order of registers wider than the bus must be explicit."""
import re

import pytest

from helpers import CASES, run_wbgenplus


def _variant(tmp_path, src, wordorder):
    """Copy case `src` with the wordorder attribute removed, or set to `wordorder`."""
    text = re.sub(r'\s+wordorder="[^"]*"', "", (CASES / f"{src}.xml").read_text())
    if wordorder is not None:
        text = text.replace("<slaveinterface ", f'<slaveinterface wordorder="{wordorder}" ', 1)
    xml = tmp_path / "in" / f"{src.split('/')[-1]}.xml"
    xml.parent.mkdir()
    xml.write_text(text)
    return xml


@pytest.mark.parametrize("src", ["prod/dm_diag", "edge/wide_high", "simple_demo"])
def test_missing_wordorder_is_an_error(src, tmp_path):
    proc, out = run_wbgenplus(_variant(tmp_path, src, None), tmp_path / "run")
    assert proc.returncode != 0
    assert "wider than the 32 bit bus" in proc.stderr
    assert not any(k.endswith(".vhd") for k in out), "no output may be written on error"


def test_invalid_wordorder_is_an_error(tmp_path):
    proc, out = run_wbgenplus(_variant(tmp_path, "edge/wide_high", "big"), tmp_path / "run")
    assert proc.returncode != 0
    assert "wordorder <big> is invalid" in proc.stderr
    assert not out


def test_wordorder_not_needed_without_multiword_registers(tmp_path):
    proc, _ = run_wbgenplus(_variant(tmp_path, "prod/oled", None), tmp_path / "run")
    assert proc.returncode == 0, proc.stdout + proc.stderr
