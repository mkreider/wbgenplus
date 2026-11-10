# wbgenplus review: handover

Working notes for the review and repair of wbgenplus, written for whoever picks this up next (Mathias, or an agent in the GHDL/cocotb container). The `review/` directory only exists on the branch: **remove it before merging to master.**

State as of 2026-11-10: branch `review/phase0`, head `1d0515c` plus this commit, pushed to `origin` (github.com/mkreider/wbgenplus).

## Ground rules (agreed with Mathias)

- Work on branches. **No push without asking Mathias**, except when he says so.
- One small commit per finding. A commit that changes generator output updates the golden files in the same commit, and the commit message explains why.
- Every bug fix comes with a test that fails on the old code.
- Production XMLs must keep regenerating byte-identical outputs (`test_production.py`).

## Environment

The tests expect this layout. Paths can be overridden:

```
<root>/                     # was ~/projects/wbgen-ws, a plain folder (not a repo)
├── wbgenplus/              # this repo
├── bel_projects/           # GSI-CS-CO/bel_projects with submodules; override: WBGEN_BEL_PROJECTS=/path
└── tools/venv/             # pytest; override: make test PYTEST=pytest
```

- **bel_projects** provides the VHDL dependencies through its general-cores submodule (pinned `9467ead`): `modules/wishbone/wbgenplus/wbgenplus_pkg.vhd` (matrix helpers), `modules/wishbone/wishbone_pkg.vhd` (`f_wb_wr`, `wb_skidpad` component), `wb_register/wb_skidpad.vhd`, `genrams/genram_pkg.vhd`. It also holds the production `*_auto*.vhd` files that `test_production.py` compares against. Tested with bel_projects `fe0c1adc0`.
- **GHDL 6.0.0** (mcode), flags `--std=08 -frelaxed -Wno-hide`. general-cores only gives `-Whide` warnings.
- **Python 3.14**, pytest 9.2. No other dependencies. cocotb is not used yet.
- Without GHDL or bel_projects, the affected tests are **skipped**, not failed; check `-rs` output.

Commands (in `wbgenplus/`):

```sh
make test     # pytest -q -rxXs: golden, production, GHDL, error and CLI tests
make golden   # regenerate tests/golden after a deliberate output change; commit the diff
```

Status: **84 passed, 2 xfailed** (strict; both are the paged-register demos, finding 1.5).

## Test suite

| File | Checks |
|---|---|
| `test_golden.py` | Output of every `tests/cases/**.xml` is byte-identical to `tests/golden/`. `SOURCE_DATE_EPOCH=1700000000`; hash-seed independent |
| `test_production.py` | dm_diag, eca_tap, oled, prio: `*_auto.vhd`/`*_auto_pkg.vhd` identical to bel_projects (date lines ignored). All 8 pass |
| `test_ghdl.py` | Analyse pkg, core and stub, elaborate `<unit>_auto`. xfail: complex_demo, intermediate_demo (paged, 1.5; complex also 1.2) |
| `test_wordorder.py`, `test_parser_errors.py`, `test_paths.py`, `test_cli.py` | Error handling, paths and CLI (see findings) |

Cases: `tests/cases/` holds the 3 demos (copies of the repo-root demos; keep them in sync), `prod/` (8 production XMLs; see `prod/SOURCE.md` for the only edits) and `edge/` (single_register, wide_high, wide_low, reset_comment).

## Done (branch commits, oldest first)

| Commit | Finding | Change |
|---|---|---|
| `fb23747` | Phase 0 | `SOURCE_DATE_EPOCH` support (output unchanged when unset) |
| `9a29212`, `3a65a70` | Phase 0 | Golden, production and GHDL tests; Makefile |
| `46d52e5` | 1.15 | Address constants zero-padded to as many as 75 digits: true division `/` from the **Python 3 port** in the format width. Now `//` |
| `4e44399` | 1.16, 1.9 | Address width from the last byte of the last register: SDB `addr_last` no longer drops a last register that starts on a power of two (oled); a single register at 0 no longer crashes |
| `844ccb5` | 1.13 | `<slaveinterface wordorder="high\|low">`, **mandatory** when there are registers wider than the bus (decided by Mathias: explicit, no default). History: b228faf (2018-07) high first, dc5f889 (2020-02) reverted it, so production has both: dm_diag and eca_tap high, prio and ebm low. `WbRegister._words()` keeps index, width and slice together (b228faf would have produced out-of-range slices for, e.g., 48-bit registers) |
| `7fe2f12` | 1.7 | Output paths via `os.path.join` (before: `x/y.xml` wrote `xy_auto.vhd` into the parent, and the stub guard checked the wrong path, so a stub could be overwritten without `-f`); `fo.close()` |
| `6dead51` | 1.3, 1.4, 1.10, 1.14, 1.17 | `errors.py` (`WbgenError`/`fail`): `ERROR:` on stderr, exit 2, nothing written. Mask must be 2ⁿ−1; bits and pages must be a number or a declared generic; invalid address, data, productID and reset are errors; `reset="ones"/"zeroes"` implemented; `%` in comments escaped in the multi-stage templates (the C header has three stages); duplicate register names and register named like the interface are rejected. complex_demo now declares `flags` |
| `6f96e75` | 1.8 | Exactly one `<slaveinterface>` (no XML in bel_projects or its submodules has more) |
| `1d0515c` | 1.11 | argparse: options anywhere, `--version` exact (no abbreviations), `-q` implemented, `-l` removed, missing file exits 2 |

### Changes needed in production repos (local only, NOT pushed)

With the new generator, the production XMLs only regenerate when they carry `wordorder` (and dm_diag drops its undeclared `pages="channels"`). The generated files do not change. The patches are in `review/patches/`:

- `bel_projects-wbgenplus-wordorder.patch`: 2 commits against bel_projects master (local branch `wbgenplus-wordorder`, `50feaa537` and `f1a109f6f`): dm_diag and eca_tap `high`, prio `low`; dm_diag without `pages`.
- `etherbone-core-wbgenplus-wordorder.patch`: 1 commit (`ec17aa7`): ebm `low`.

The submodule pointer in bel_projects is deliberately not committed. Applying these patches is Mathias' call.

## Open findings (next steps, in order)

### 1.1 `drive` + `clock=` has no clock-domain crossing
`wbslave.py` around L111-118: `if reg.isDrive(): … elif reg.isSync(): if reg.isDrive(): …`, so the inner sync branch for driven registers can never run. The input goes straight into the sys domain without a synchroniser, and the valid flag `*_V_*_i` has none either. Introduced in 2cd8c40 (2016-03-29). **No production XML uses `clock=`**, so this is latent. complex_demo has `status` with `clock="ref"`.

### 1.2 Write-side backpressure and autostall
In the FIFO and flow-control templates (`stringtemplates.py` around L94/156 and L345-395): `g_with_wr_almost_full => true`, but `wr_almost_full_o` is not connected; `s_stall <= s_full` ignores autostall; `r_stall` is referenced (complex_demo) but never declared, so GHDL fails. Lost in d0943e4 (2016-04-06). Only the v1 generator (`eca_ac_wbm`) uses autostall in production.

**Plan for 1.1/1.2: cocotb tests** (agreed). (a) A value and valid flag driven in the `ref` domain arrive correctly in the sys domain. (b) The bus stalls when the write FIFO is (almost) full, and for one cycle after an access to an autostall register. Then the GHDL xfail for complex_demo should only hit 1.5.

### 1.5/1.6 Paged registers never compile
`r_p`/`v_p` are not declared (`wbsPageSelect` L473 assigns `r_p <=`; the matrix templates L300-302 use `v_p`/`r_p`); the `wbOutMatrix` arguments are swapped (`c_r_ts_out_GET_0`, `mget(ts_out, …)`); `(others => '0')` is used as init for a 2D `matrix`. Caused by 2cd8c40 (2016) and 17e9f41 (2018, "untested"). Last tested version: 3b73e68 (2015, cocotb + Questa). Not used in production (dm_diag's `paged="yes"` never took effect). Fix, remove the GHDL xfails, and add a cocotb test for page selection. Alternative to discuss with Mathias: drop paging.

### 1.18 (suspected) bus widths other than 32
`wbslave.getSkidPad` has `g_adrbits => maxAdr-2` hardcoded, and `stringtemplates.py` L371 has `s_a_ext <= s_a & "00"`. That assumes 4 bytes per word. `data` currently accepts any multiple of 8. Check with a `data="64"` (and 16) edge case in GHDL; then either fix it or restrict `data` to 32.

### 1.12 Documented but ignored
`wbdevice unitname`, `<codegen>`, `type="classic"`, sdb `version`/`date`. Implement or remove from the help text. (reset ones/zeroes is done.)

## Later phases

- **Phase 2, cleanup (golden files must stay identical):** dead code (`wbsCStr`, `readUpdate`, `portsignameout`, `sl`, `wbStall`, `slaveSigs`, `wbs_reg_o/i`, `sdbReference`, `codeGen`, `genTypes`, `instGen*`, `componentMid`, `headerDetails`, `wbReadMatrix`, the `padding` variable, the no-op `s.append` in register.py, commented-out blocks, unused imports such as `mskWidth` in wbgenplus.py); `is*()` becomes `'w' in self.flags`; table-driven flag parsing; merge the duplicated pages/selector branches; typos ("Pyhton", "zereos", "seperate", "follwing"); stale version strings (0.7 / 2015); port-list blank-line grouping. `textformatting.mskWidth` is only used for **addresses** now (ceil(log2)); rename it and keep the behaviour (bit_length would change padding, and the oled match would break).
- **Phase 3, structure:** parse, then a validated model (dataclasses, typed flags), then separate VHDL, C and Python emitters, without format-string-on-format-string templates (the root cause of the `%` bug). `with open`; `pyproject.toml` with a `wbgenplus` entry point. Open: stay dependency-free or use Jinja2?
- **Phase 4, docs:** README (usage, outputs, VHDL deps), the XML reference moved from `stringtemplates.py` into `docs/`, an XSD, a changelog.
- **Further open questions:** the hardcoded GSI copyright and LGPL header in every output file; the generation date in the output and the SDB record (now controllable via `SOURCE_DATE_EPOCH`).
