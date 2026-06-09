# Day 8 - Simple PubChem Web App

This project is based on the day 6 PubChem amphiphile program.

The day 6 folder was not changed.

## What The Program Does

The program looks up amphiphile compounds in PubChem.

The web page lets the user choose compounds from a starter list and also type
other compound names.

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

## Setup

From the `day08` folder:

```bash
python -m venv .venv
```

```bash
.\.venv\Scripts\Activate.ps1
```

```bash
python -m pip install -r requirements.txt
```

## Run The Web App

From the `day08` folder:

```bash
python web_app.py
```

Or:

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
python -m pytest
```

The tests use fake PubChem data, so they do not need the internet.

## Prompts

### Prompt 1

Please create the following in the day8 folder and take the files from day 6
folder. Do not change anything in the day 6 folder.

Make sure it has a "business logic" part that is tested.

Write a web application for it. You can use Flask but it would be nicer if you
used one of the other web frameworks of Python.

Make sure they use the same "business logic" functions.

Write some tests for the web application as well.

Include your prompts as well.

### Prompt 2

Use the day 6 PubChem amphiphile script as the starting point, but refactor the
day 8 copy so the PubChem lookup and data extraction live in importable business
logic functions. Then make both the plotting script and the web application call
those same functions.

### Prompt 3

Add pytest tests that avoid real PubChem network calls by using fake response
objects. Test the business logic directly and test the web API with an injected
fake lookup function.

### Prompt 4

This seems way too elaborate for the stage of the course I am at. Can it be much
simpler so I can comprehend what is going on?

### Prompt 5

i dont know what sandbox is. also the app should allow to chose any kind of
amphiphile and not just these ones no? or at least able to choose from the list
of compounds

### Prompt 6

promppts should appear in the readme file not standalone
