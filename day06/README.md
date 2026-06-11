# Day 6 - PubChem Amphiphile Analysis

This program looks up amphiphile compounds in PubChem and plots two molecular
properties:

- `TPSA` - topological polar surface area
- `XLogP` - octanol-water partition coefficient

## Business Logic

The reusable business logic is in `compound_logic.py`.

That file contains the functions that:

- load the compound names
- look up one compound in PubChem
- look up many compounds
- separate found compounds from skipped compounds

The original plot program, `pubchem_amp.py`, uses that business logic instead of
doing the PubChem lookup directly inside the plotting code.

## Files

- `compound_logic.py` - business logic for PubChem data.
- `pubchem_amp.py` - the plotting program.
- `test_pubchem_amp.py` - tests for the business logic.
- `requirements.txt` - packages needed for this day.

## Run The Program

From the `day06` folder, run:

```text
python pubchem_amp.py
```

## Run The Tests

From the `day06` folder, run:

```text
python -m pytest
```

The tests use fake PubChem data, so they do not need the internet.

## Background

PubChem is a public chemical database maintained by the National Center for
Biotechnology Information. It contains information about chemical compounds,
including molecular properties.

XLogP is an estimated logarithm of the octanol-water partition coefficient. It
helps describe how hydrophobic or hydrophilic a molecule is.

TPSA stands for topological polar surface area. It helps describe the polar
surface area of a molecule.

Amphiphiles contain both hydrophilic and hydrophobic parts. This makes them
relevant to self-assembly, GARD, and Lipid World ideas.
