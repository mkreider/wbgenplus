# Production XML test inputs

These are verbatim copies of the wbgenplus v2 inputs used in production, taken on 2026-11-03 from:

| File | Origin (relative to bel_projects `fe0c1adc0`) |
|---|---|
| dm_diag.xml | `modules/dm_diag/` |
| eca_tap.xml | `modules/eca_tap/` |
| oled.xml | `modules/oled_display/` |
| prio.xml | `modules/prioq2/` |
| eca.xml, eca_queue.xml, eca_tlu.xml | `ip_cores/wr-cores/modules/wr_eca/` (wr-cores `76c4b10e`) |
| ebm.xml | `ip_cores/etherbone-core/hdl/eb_master_core/` (etherbone-core `7a4c0a3e`) |

`eca_ac_wbm.xml` is left out on purpose: it was written for the v1 generator (2014), which used attributes such as `weflag` that v2 does not support.

**Only change from the originals:** `wordorder` was added to `<slaveinterface>`, because it has been mandatory for registers wider than the bus since finding 1.13. The values reproduce the committed production outputs:

| File | wordorder | Reason |
|---|---|---|
| dm_diag.xml, eca_tap.xml | `high` | generated between b228faf (2018-07) and dc5f889 (2020-02) |
| prio.xml, ebm.xml | `low` | generated before 2018-07 |

The other files have no multi-word registers and are unchanged. Make no other edits; a fix that needs a changed input gets its own case.
