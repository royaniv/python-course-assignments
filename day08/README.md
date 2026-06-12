# Day 8 - Simple PubChem Amphiphile Program

This project is based on the day 6 PubChem amphiphile program.

The goal is to keep the assignment valid while using simple Python that is easy
to follow. The web app uses the FastAPI web framework, and day 8 can run without
access to the day 6 folder.

## What The Programs Do

The programs look up amphiphile compounds in PubChem.

For each compound, the code tries to get:

- `TPSA` - topological polar surface area
- `XLogP` - octanol-water partition coefficient

If PubChem has both values, the compound is used. If one value is missing, the
compound is skipped.

The results are shown as a table and as a plot of TPSA against XLogP.

## Files

- `web_app.py` - the main beginner-friendly web app. Run this file to use the browser page.
- `pubchem_amp.py` - a simpler plot-only script.
- `compound_logic.py` - the day 8 business logic for compound names and PubChem data.
- `plot_logic.py` - makes the SVG plot used on the web page.
- `styles.css` - styling for the web page.
- `requirements.txt` - Python packages needed for this project.
- `test_pubchem_amp.py` - tests for the business logic.
- `test_web_app.py` - tests for the web page functions.
- `CODE_EXPLANATION.md` - a longer explanation of the code.

The business logic in `compound_logic.py` is the day 8 copy of the day 6 logic.

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
http://127.0.0.1:8001
```

The web page lets you choose compounds from the built-in list and also type other
PubChem compound names.

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

- `web_app.py` handles the browser page and web server.
- `pubchem_amp.py` handles the plot-only version.
- `compound_logic.py` handles compound names and PubChem data.

The business logic matches day 6 because `compound_logic.py` was copied from the day 6 logic.

## Prompts


Please copy day 6 and create a web application using a web framework for it in the day8 folder and take the files from day 6 folder. Do not change anything in the day 6 folder.

Make sure it has a "business logic" part that is tested.

Write some tests for the web application as well.


