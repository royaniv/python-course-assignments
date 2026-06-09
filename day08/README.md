# Day 8 - Simple PubChem Web App

This project is based on the day 6 PubChem amphiphile program.

The day 6 folder was not changed.

## What The Program Does

The program looks up amphiphile compounds in PubChem.

For each compound, it tries to get:

- `TPSA`
- `XLogP`

If PubChem has both values, the compound is shown in the results.

If one of the values is missing, the compound is skipped.

## Files

- `compound_logic.py` - the business logic.
- `pubchem_amp.py` - a script that makes a matplotlib plot.
- `web_app.py` - the web application.
- `test_pubchem_amp.py` - tests for the business logic.
- `test_web_app.py` - tests for the web application.
- `prompts.md` - prompts used for the assignment.

## Run The Web App

From the `day08` folder:

```bash
uvicorn web_app:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## Run The Plot Version

```bash
python pubchem_amp.py
```

## Run The Tests

```bash
pytest
```

The tests use fake PubChem data, so they do not need the internet.
