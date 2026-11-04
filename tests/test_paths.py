"""Finding 1.7: output files land next to the XML, however its path is given."""
import pytest

from helpers import CASES, GOLDEN, run_wbgenplus


@pytest.mark.parametrize("invoke", ["relative", "absolute"])
@pytest.mark.parametrize("case", ["simple_demo", "prod/oled"])
def test_output_next_to_xml(case, invoke, tmp_path):
    proc, out = run_wbgenplus(CASES / f"{case}.xml", tmp_path, invoke=invoke)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    stray = [k for k in out if k.startswith("../")]
    assert not stray, f"files written outside the XML's directory: {stray}"
    expected = {p.name: p.read_text() for p in (GOLDEN / case).iterdir()}
    assert sorted(out) == sorted(expected)
    for name, text in expected.items():
        assert out[name].decode() == text, f"{name} differs from golden"


def test_existing_stub_is_kept_without_force(tmp_path):
    xml = CASES / "simple_demo.xml"
    work = tmp_path / "work"
    work.mkdir()
    (work / "simple_demo.vhd").write_text("-- my edits\n")
    proc, out = run_wbgenplus(xml, tmp_path, invoke="relative")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (work / "simple_demo.vhd").read_text() == "-- my edits\n"
    assert "already exists" in proc.stdout
