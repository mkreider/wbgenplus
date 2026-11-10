"""Findings 1.3, 1.4, 1.10, 1.14, 1.17: invalid input is a clear error, never a crash
or a silent fallback. On error the exit status is 2, stderr starts with "ERROR:",
there is no traceback, and nothing is written."""
import pytest

from helpers import run_wbgenplus

TEMPLATE = """<wbdevice author="T" email="t@x" version="0.0.1">
   <clockdomain name="sys"></clockdomain>
   {generics}
   <slaveinterface name="ctrl" {slave}>
      <sdb vendorID="GSI" productID="{product}" version="1" date="auto" name="ERRTEST"></sdb>
      <registers>
         {regs}
      </registers>
   </slaveinterface>
</wbdevice>
"""
OK_REG = '<reg name="a" read="yes" write="yes" bits="8" comment="ok"></reg>'


def _xml(tmp_path, generics="", slave='data="32"', product="0x1", regs=OK_REG):
    p = tmp_path / "in" / "errtest.xml"
    p.parent.mkdir(exist_ok=True)
    p.write_text(TEMPLATE.format(generics=generics, slave=slave, product=product, regs=regs))
    return p


def _reg(**attrs):
    attrs.setdefault("name", "b")
    attrs.setdefault("comment", "c")
    return OK_REG + " <reg " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "></reg>"


ERRORS = {
    # 1.3 mask must be 2^n-1
    "mask_gap":          (dict(regs=_reg(read="yes", mask="0x80")), "must be a contiguous bitmask"),
    "mask_hole":         (dict(regs=_reg(read="yes", mask="0xf0f")), "must be a contiguous bitmask"),
    "mask_garbage":      (dict(regs=_reg(read="yes", mask="zz")), "must be a contiguous bitmask"),
    # 1.4 bits: number or declared generic
    "bits_undeclared":   (dict(regs=_reg(read="yes", bits="flags")), "bits <flags> is neither"),
    "bits_zero":         (dict(regs=_reg(read="yes", bits="0")), "bits <0> is neither"),
    "generic_bad":       (dict(generics='<generic name="g" type="natural" default="x" comment="c"></generic>'), "default <x> is not a valid natural"),
    "generic_twice":     (dict(generics='<generic name="g" type="natural" default="1" comment="c"></generic>' * 2), "declared twice"),
    # 1.14 pages: number or declared generic
    "pages_undeclared":  (dict(slave='data="32" pages="channels"'), "pages <channels> is neither"),
    # 1.10 parser crashes
    "address_garbage":   (dict(regs=_reg(read="yes", address="foo")), "address <foo> is invalid"),
    "address_overlap":   (dict(regs=_reg(read="yes", address="0x0")), "overlaps the previous register"),
    "data_garbage":      (dict(slave='data="x"'), "data <x> must be a positive multiple of 8"),
    "data_not_bytes":    (dict(slave='data="12"'), "data <12> must be a positive multiple of 8"),
    "product_garbage":   (dict(product="zz"), "Invalid Product ID <zz>"),
    "reset_garbage":     (dict(regs=_reg(read="yes", write="yes", reset="lots")), "reset <lots> is invalid"),
    # 1.17 name collisions
    "reg_named_like_if": (dict(regs=_reg(name="ctrl", read="yes")), "same name as its slave interface"),
    "reg_twice":         (dict(regs=_reg(name="a", read="yes")), "register <a> is declared twice"),
}


@pytest.mark.parametrize("kwargs,message", ERRORS.values(), ids=ERRORS.keys())
def test_invalid_input_is_reported(kwargs, message, tmp_path):
    proc, out = run_wbgenplus(_xml(tmp_path, **kwargs), tmp_path / "run")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert proc.stderr.startswith("ERROR:"), proc.stderr
    assert message in proc.stderr
    assert "Traceback" not in proc.stderr
    assert not out, f"nothing may be written on error, got {list(out)}"


def test_malformed_xml_is_reported(tmp_path):
    p = _xml(tmp_path)
    p.write_text(p.read_text().replace("</wbdevice>", ""))
    proc, out = run_wbgenplus(p, tmp_path / "run")
    assert proc.returncode == 2
    assert "is not well-formed XML" in proc.stderr
    assert not out


@pytest.mark.parametrize("kwargs", [
    dict(slave=""),                                     # data defaults to 32
    dict(regs=_reg(read="yes", mask="0x1")),            # 1-bit mask
    dict(regs=_reg(read="yes", mask="0xffffffff")),
    dict(regs=_reg(read="yes", write="yes", reset="ones")),
    dict(regs=_reg(read="yes", write="yes", reset="zeroes")),
], ids=["data_default", "mask_1", "mask_32", "reset_ones", "reset_zeroes"])
def test_valid_input_is_accepted(kwargs, tmp_path):
    proc, out = run_wbgenplus(_xml(tmp_path, **kwargs), tmp_path / "run")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "errtest_auto.vhd" in out
