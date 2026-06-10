# Day 8 Code Explanation

This document explains the files in the `day08` folder.

The program is split only where it helps:

- `compound_logic.py` contains the reusable PubChem/data logic.
- `web_app.py` contains the browser app.
- `styles.css` contains the web page styling.
- `pubchem_amp.py` contains the separate matplotlib plot version.
- the test files check that the logic works without using the real internet.

This keeps the project smaller than the earlier refactor, but still avoids one
huge function.

## Which File Is The Actual Program?

There are two files you can run:

- `web_app.py` is the main web program. Run this when you want the browser app.
- `pubchem_amp.py` is the plot-only program. Run this when you want a matplotlib
  plot window.

The other files support those programs:

- `compound_logic.py` is imported by both programs.
- `styles.css` is loaded by the web page.
- `compound_list.txt` supplies the dropdown/list of compounds.
- the `test_...py` files are run by pytest.
- `README.md` and `CODE_EXPLANATION.md` are explanations.

So for normal use, the most important command is:

```bash
python web_app.py
```

Then open:

```text
http://127.0.0.1:8000
```

## `compound_logic.py`

This is the business logic file. It does not create the web page. It handles
compound names and PubChem data.

### `load_compound_list`

Reads compound names from `compound_list.txt`.

If the file exists and has names in it, it returns those names as a list. If the
file is missing or empty, it returns an empty list.

### `get_compound_names`

Turns typed text into a list of compound names.

It accepts both commas and new lines, so this:

```text
octanol
decanol, oleic acid
```

becomes:

```python
["octanol", "decanol", "oleic acid"]
```

### `choose_compound_names`

Combines names selected from the dropdown with names typed by the user.

It removes duplicates so the same compound is not looked up twice.

### `get_pubchem_data`

Looks up one compound in PubChem.

It asks PubChem for:

- `TPSA`
- `XLogP`

If both values exist, it returns a dictionary:

```python
{
    "name": "octanol",
    "tpsa": 20.2,
    "xlogp": 2.9,
}
```

If the compound cannot be used, it returns `None`.

### `get_many_compounds`

Looks up several compounds.

It returns two lists:

- found compounds
- skipped compounds

## `web_app.py`

This file contains the web application.

It imports the business logic from `compound_logic.py`, then builds a simple
HTML page using Python strings.

### `make_compound_options`

Builds the dropdown options from `compound_list.txt`.

### `make_plot_svg`

Builds a simple SVG scatter plot for the browser.

The x-axis is TPSA. The y-axis is XLogP. The table shows the compound names, so
the plot only draws points. This keeps the plot less crowded.

### `make_results_html`

Builds the results section after the user submits the form.

It includes:

- the result count
- a table of compounds
- skipped compound names
- the SVG plot

### `make_page`

Builds the complete HTML page.

It includes the title, form, dropdown, text area, button, and results section.
The styling is not inside this function; it is in `styles.css`.

### `make_page_from_query`

Reads the browser query string.

If the form was submitted, it:

1. gets selected compounds
2. gets typed compound names
3. combines them
4. calls PubChem through `get_many_compounds`
5. returns the completed HTML page

### `AmphiphileHandler`

Handles browser requests.

It serves:

- `/` for the web page
- `/styles.css` for the CSS file

### `run_server`

Starts the local web server at:

```text
http://127.0.0.1:8000
```

The bottom of the file has:

```python
if __name__ == "__main__":
    run_server()
```

This starts the server only when `web_app.py` is run directly.

## `styles.css`

This file contains the web page design.

It controls:

- colors
- spacing
- the form layout
- the table
- the plot
- small-screen layout

Keeping CSS outside Python makes `web_app.py` much shorter.

## `pubchem_amp.py`

This is the command-line plot version.

It uses the same business logic as the web app:

```python
from compound_logic import get_many_compounds, load_compound_list
```

It loads the compound list, gets PubChem data, and shows a matplotlib plot.

## Tests

The tests use fake PubChem responses, so they do not need the internet.

### `test_pubchem_amp.py`

Tests the business logic:

- splitting compound names
- reading PubChem-style data
- handling missing data
- handling request errors
- separating found and skipped compounds

### `test_web_app.py`

Tests the web page functions:

- selected and typed names are combined
- the home page has a form
- the results page shows data
- the query string creates a results page

## Why This Version Is Smaller

The previous refactor had extra files for HTML and SVG plot logic. That was
organized, but probably too much for this assignment.

This version keeps only one important separation:

- `compound_logic.py` = data/PubChem logic
- `web_app.py` = web page and server

That is simpler to explain while still avoiding one very long `main` function.
