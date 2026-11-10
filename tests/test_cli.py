"""Finding 1.11: command line handling (argparse)."""
import os
import subprocess
import sys

import pytest

from helpers import CASES, REPO, SOURCE_DATE_EPOCH, run_wbgenplus


def _cli(*args, cwd):
    env = dict(os.environ, SOURCE_DATE_EPOCH=SOURCE_DATE_EPOCH, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([sys.executable, str(REPO / "wbgenplus.py"), *args],
                          cwd=cwd, env=env, capture_output=True, text=True, timeout=60)


def test_no_arguments_shows_usage(tmp_path):
    r = _cli(cwd=tmp_path)
    assert r.returncode == 2
    assert "usage: wbgenplus.py" in r.stderr


def test_missing_file_is_an_error(tmp_path):
    r = _cli("nope.xml", cwd=tmp_path)
    assert r.returncode == 2
    assert r.stderr.startswith("ERROR: file not found: nope.xml")


@pytest.mark.parametrize("opt", ["-l", "--log", "--vers", "-x"])
def test_unknown_or_abbreviated_option_is_rejected(opt, tmp_path):
    r = _cli(opt, "x.xml", cwd=tmp_path)
    assert r.returncode == 2
    assert "unrecognized arguments" in r.stderr or "the following arguments are required" in r.stderr


@pytest.mark.parametrize("opt,text", [("--version", "wbgenplus - A Wishbone Slave Generator"),
                                      ("-h", "wbgenplus Manual"), ("--help", "wbgenplus Manual")])
def test_info_options_work_without_a_file(opt, text, tmp_path):
    r = _cli(opt, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    assert text in r.stdout


@pytest.mark.parametrize("args", [("-q",), ("-q", "-f")])
@pytest.mark.parametrize("before", [True, False], ids=["options_first", "options_last"])
def test_options_before_or_after_the_file(args, before, tmp_path):
    xml = CASES / "simple_demo.xml"
    (tmp_path / "work").mkdir()
    (tmp_path / "work" / xml.name).write_text(xml.read_text())
    argv = [*args, "work/simple_demo.xml"] if before else ["work/simple_demo.xml", *args]
    r = _cli(*argv, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "", "quiet mode must not print"
    assert (tmp_path / "work" / "simple_demo_auto.vhd").is_file()


def test_force_overwrites_stub_and_quiet_keeps_errors(tmp_path):
    xml = CASES / "simple_demo.xml"
    work = tmp_path / "work"
    work.mkdir()
    (work / "simple_demo.vhd").write_text("-- my edits\n")
    proc, out = run_wbgenplus(xml, tmp_path, args=("-f",), invoke="relative")
    assert proc.returncode == 0
    assert (work / "simple_demo.vhd").read_text() != "-- my edits\n"

    bad = work / "bad.xml"
    bad.write_text(xml.read_text().replace('wordorder="high"', 'wordorder="big"'))
    r = _cli("-q", str(bad), cwd=tmp_path)
    assert r.returncode == 2
    assert r.stdout == ""
    assert r.stderr.startswith("ERROR:")
