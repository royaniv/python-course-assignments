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
- `../day06/compound_logic.py` - the exact business logic used by day 6 and day
  8.
- `styles.css` - styling for the web page.
- `requirements.txt` - Python packages needed for this project.
- `test_pubchem_amp.py` - tests for the business logic.
- `test_web_app.py` - tests for the web page functions.
- `CODE_EXPLANATION.md` - a longer explanation of the code.

You do not run `../day06/compound_logic.py`, `styles.css`, the test files, or
the documentation files directly.

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

The web page lets you choose compounds from the day 6 list and also type other
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

- `../day06/compound_logic.py` handles compound names and PubChem data.
- `web_app.py` handles the browser page and web server.
- `pubchem_amp.py` handles the plot-only version.

Day 8 does not have its own copy of the business logic. Both runnable day 8
programs import and call `get_many_compounds` from `../day06/compound_logic.py`.

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

### Prompt 7

all of this sounds too elaborate for a day 8 assignment no?

### Prompt 8

so i would like you to look at day1-7 and see if you can create something much
simpler for day 8 but keeping the requested assignemnet valid

### Prompt 9

where is the plot that i asked for i dont see it being created?

### Prompt 10

arent there too many subfucntions and things in day 8 can it not be minmized?

### Prompt 11

redo day 6 to have business logic and then use the exact same business logic in
day 8 please
