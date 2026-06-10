# Day 8 - Simple PubChem Amphiphile Program

This project is based on the day 6 PubChem amphiphile program.

The goal is to keep the assignment valid while using simple Python that is easy
to follow. The web app uses Python's built-in `http.server`, not FastAPI, Flask,
uvicorn, or httpx.

## What The Programs Do

The programs look up amphiphile compounds in PubChem.

For each compound, the code tries to get:

- `TPSA` - topological polar surface area
- `XLogP` - octanol-water partition coefficient

If PubChem has both values, the compound is used. If one value is missing, the
compound is skipped.

The results are shown as a table and as a plot of TPSA against XLogP.

## Files

- `web_app.py` - the main web app. Run this file to use the browser page.
- `pubchem_amp.py` - a simpler plot-only script.
- `compound_logic.py` - shared business logic used by both programs.
- `compound_list.txt` - example amphiphile names for the dropdown menu.
- `styles.css` - styling for the web page.
- `requirements.txt` - Python packages needed for this project.
- `test_pubchem_amp.py` - tests for the business logic.
- `test_web_app.py` - tests for the web page functions.
- `CODE_EXPLANATION.md` - a longer explanation of the code.

You do not run `compound_logic.py`, `styles.css`, `compound_list.txt`, the test
files, or the documentation files directly.

## Setup

Open a terminal in the `day08` folder and install the needed packages:

```text
python -m pip install -r requirements.txt
```

You only need to do this setup step when the packages are not installed yet.

## Run The Web App

From the `day08` folder, run:

```text
python web_app.py
```

Then open this address in a browser:

```text
http://127.0.0.1:8000
```

The web page lets you choose compounds from the list and also type other PubChem
compound names.

## Run The Plot-Only Script

If you only want the matplotlib plot and not the web page, run:

```text
python pubchem_amp.py
```

## Run The Tests

From the `day08` folder, run:

```text
python -m pytest
```

The tests use fake PubChem data, so they do not need the internet.

## Code Structure

The project keeps one main separation:

- `compound_logic.py` handles compound names and PubChem data.
- `web_app.py` handles the browser page and web server.
- `pubchem_amp.py` handles the plot-only version.

This way, the same business logic is reused by the web app, the plot script, and
the tests.
