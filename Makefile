# Test targets. pytest is expected in ../tools/venv (override with PYTEST=...).
PYTEST ?= ../tools/venv/bin/pytest

.PHONY: test golden

# Golden files, production comparison (../bel_projects) and GHDL compile
test:
	$(PYTEST) -q -rxXs

# Regenerate golden files after a deliberate output change; commit the diff with the change
golden:
	WBGEN_UPDATE_GOLDEN=1 $(PYTEST) -q tests/test_golden.py
