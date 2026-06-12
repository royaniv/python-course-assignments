# Day 8 Code Explanation

This document explains every Python file in the `day08` folder.

day08 can run by itself. It has copied `compound_logic.py` from day06.

## File Overview

- `compound_logic.py` contains the business logic: compound names, PubChem
  requests, and extracting TPSA/XLogP values.
- `plot_logic.py` creates the SVG plot used inside the web page.
- `web_app.py` creates the FastAPI web app.
- `pubchem_amp.py` creates the separate matplotlib plot-only program.
- `test_pubchem_amp.py` tests the business logic and plot-only program.
- `test_web_app.py` tests the FastAPI web app.

The normal web app command is:

```text
python web_app.py
```

Then open:

```text
http://127.0.0.1:8001
```

## `compound_logic.py`

This is the business logic file. It  handles compound names and PubChem data.

### Imports

```python
from urllib.parse import quote

import requests
```

- `quote` makes compound names safe to put into a URL. For example, it can make spaces work correctly in a web address.
- `requests` is used to ask PubChem for compound data.

### `DEFAULT_COMPOUNDS`

```python
DEFAULT_COMPOUNDS = [...]
```

This is the built-in list of amphiphile compounds shown in the web page
dropdown.

### `load_compound_list`

```python
def load_compound_list():
```

This function returns a copy of the built-in compound list.

The `.copy()` matters because it returns a new list, not the original list.

### `get_compound_names`

```python
def get_compound_names(text):
```

This function turns typed text into a Python list of compound names.

If the user did not type anything, the function returns an empty list:

```python
if text is None:
    return []
```

Then commas are treated like new lines:

```python
text = text.replace(",", "\n")
```

So this:

```text
octanol
decanol, dodecanol
```

becomes:

```python
["octanol", "decanol", "dodecanol"]
```

The loop checks every line, removes extra spaces, and keeps only non-empty
names.

### `choose_compound_names`

```python
def choose_compound_names(selected_compounds=None, compound_text=""):
```

This function combines two sources:

- compounds selected from the dropdown
- compounds typed into the text box

It first adds selected compounds if there are any. Then it calls
`get_compound_names(compound_text)` to add typed compounds.

The final loop removes duplicates:

```python
for name in names:
    if name not in unique_names:
        unique_names.append(name)
```

That means if `octanol` is selected and also typed, it is only looked up once.

### `get_pubchem_data`

```python
def get_pubchem_data(compound, requests_get=requests.get):
```

This function looks up one compound in PubChem.

The second parameter, `requests_get`, normally uses `requests.get`. It is written
as a parameter so the tests can pass in a fake request function instead of using
the real internet.

The URL asks PubChem for two properties:

- `XLogP`
- `TPSA`

The function then:

1. sends the request
2. checks that the response did not fail
3. converts the response to JSON
4. reads the first result from PubChem
5. checks that both `TPSA` and `XLogP` exist
6. returns a dictionary if the compound can be used

The returned dictionary looks like this:

```python
{
    "name": "octanol",
    "tpsa": 20.2,
    "xlogp": 2.9,
}
```

The `float(...)` calls make sure the numbers are stored as numbers, not text.

The `try`/`except` block catches problems such as:

- the request failed
- PubChem returned unexpected data
- a value was missing
- a value could not be converted to a number

If anything goes wrong, the function returns `None`.

### `get_many_compounds`

```python
def get_many_compounds(compound_names, requests_get=requests.get):
```

This function looks up several compounds.

It creates two lists:

- `found_compounds` for compounds with usable data
- `skipped_compounds` for compounds that could not be used

For each compound name, it calls `get_pubchem_data`.

If the result is `None`, the compound name goes into `skipped_compounds`.
Otherwise the result dictionary goes into `found_compounds`.

The function returns both lists:

```python
return found_compounds, skipped_compounds
```

## `plot_logic.py`

This file creates the plot that appears inside the web page. It returns SVG
text, which the browser can draw directly.

### Import

```python
from html import escape
```

`escape` protects compound names before putting them into HTML/SVG. This avoids
problems if a name contains a special character.

### Plot Constants

```python
PLOT_WIDTH = 720
PLOT_HEIGHT = 430
PLOT_LEFT = 85
PLOT_RIGHT = 30
PLOT_TOP = 40
PLOT_BOTTOM = 75
```

These numbers control the size of the SVG and the empty space around the plot.

The left and bottom spaces are larger because the axis labels need room.

### `make_plot_svg`

```python
def make_plot_svg(found_compounds):
```

This function receives the found compound dictionaries from `compound_logic.py`.

If there are no compounds, it returns an empty string:

```python
if len(found_compounds) == 0:
    return ""
```

That means no plot is shown until there is data.

The next part collects all TPSA values and XLogP values:

```python
tpsas = [compound["tpsa"] for compound in found_compounds]
xlogps = [compound["xlogp"] for compound in found_compounds]
```

Then it finds the smallest and largest values. Those values are used to scale
the points onto the SVG.

The range code prevents division by zero:

```python
tpsa_range = max(max_tpsa - min_tpsa, 1)
xlogp_range = max(max_xlogp - min_xlogp, 1)
```

If all points have the same value, the range would be zero. This code uses `1`
instead.

The min and max values are then expanded by 10 percent. This creates a little
space around the points so they are not drawn on the exact edge of the plot.

Inside the loop, each compound becomes one SVG circle:

```python
x = ...
y = ...
```

The `x` value uses TPSA. The `y` value uses XLogP. The y-axis formula looks a
little backwards because SVG y-coordinates start at the top of the image.

Each point also gets a `<title>`:

```python
<title>{name}</title>
```

Browsers often show this title when hovering over the point.

Finally, the function returns one big HTML/SVG string. It includes:

- a heading called `Plot`
- the x-axis line
- the y-axis line
- tick labels for min and max values
- all the point circles
- x-axis and y-axis labels

## `web_app.py`

This file creates the browser web app using FastAPI.

### Imports

```python
from html import escape
from pathlib import Path
from typing import List, Optional
```

- `escape` protects text before putting it into HTML.
- `Path` finds `styles.css`.
- `List` and `Optional` are type hints used in the FastAPI route.

```python
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse
```

- `FastAPI` creates the web app.
- `Query` tells FastAPI how to handle query parameters from the form.
- `HTMLResponse` tells FastAPI that a route returns HTML.
- `PlainTextResponse` is used for the CSS file.
- `uvicorn` is the server that runs the FastAPI app.

```python
import plot_logic
from compound_logic import choose_compound_names, get_many_compounds, load_compound_list
```

- `plot_logic` makes the SVG plot.
- `choose_compound_names`, `get_many_compounds`, and `load_compound_list` are
  the business logic functions from `compound_logic.py`.

### `STYLE_PATH`

```python
STYLE_PATH = Path(__file__).with_name("styles.css")
```

This finds the `styles.css` file in the same folder as `web_app.py`.

### `app`

```python
app = FastAPI()
```

This creates the FastAPI app object. The tests and `uvicorn` both use this
object.

### `make_page`

```python
def make_page(compound_text="", selected_compounds=None, found_compounds=None, skipped_compounds=None):
```

This function builds the whole HTML page as one Python string.

The parameters have default values so the same function can build:

- the empty starting page
- the results page after the form is submitted

The first line creates a set of selected compound names:

```python
selected_names = set(selected_compounds or [])
```

A set makes it easy to check whether each dropdown option should be marked as
selected.

The dropdown options are built in a loop:

```python
for name in load_compound_list():
```

For each compound, the function creates an `<option>` tag. If that compound was
already selected, it adds the word `selected` to the tag.

The table rows are built from `found_compounds`:

```python
rows = "".join(...)
```

Each found compound becomes one table row with:

- compound name
- TPSA
- XLogP

The skipped compounds are joined into one line of text:

```python
skipped_text = ", ".join(skipped_compounds) if skipped_compounds else "None"
```

The returned HTML includes:

- the document start
- a link to `/styles.css`
- the page title
- the form
- the dropdown
- the text area
- the submit button
- the results table
- the SVG plot from `plot_logic.make_plot_svg`
- the skipped compounds line

The form uses `method="get"`, which means the selected values are sent in the
URL query string.

### `home`

```python
@app.get("/", response_class=HTMLResponse)
def home(...):
```

This is the FastAPI route for the home page.

The decorator means: when the browser asks for `/`, run this function.

The parameters come from the form:

```python
submitted: Optional[str] = None
compound_text: str = ""
selected_compounds: Optional[List[str]] = Query(default=None)
```

- `submitted` tells the function whether the form was submitted.
- `compound_text` is the text typed by the user.
- `selected_compounds` is the list from the multi-select dropdown.

If the form was not submitted yet, the function returns the empty page:

```python
if submitted is None:
    return make_page()
```

If the form was submitted, the function:

1. makes sure `selected_compounds` is a list
2. combines selected and typed names with `choose_compound_names`
3. looks up PubChem data with `get_many_compounds`
4. returns the HTML page with results

### `styles`

```python
@app.get("/styles.css", response_class=PlainTextResponse)
def styles():
```

This route sends the CSS file to the browser.

The browser asks for `/styles.css` because the HTML page has:

```html
<link rel="stylesheet" href="/styles.css">
```

The function reads the CSS file and returns it with the content type
`text/css`.

### `run_server`

```python
def run_server(port=8001):
```

This function starts the local web server.

It prints the address so the user knows what to open:

```python
print(f"Starting FastAPI web app at http://127.0.0.1:{port}/")
```

Then it runs the FastAPI app with uvicorn:

```python
uvicorn.run(app, host="127.0.0.1", port=port)
```

`127.0.0.1` means the app runs on the local computer.

### Main Guard

```python
if __name__ == "__main__":
    run_server()
```

This means `run_server()` only runs when the file is started directly with:

```text
python web_app.py
```

If another file imports `web_app.py`, the server does not automatically start.
That is important for the tests.

## `pubchem_amp.py`

This is the plot-only program. It is separate from the web app.

### Import

```python
from compound_logic import get_many_compounds, load_compound_list
```

This imports the same business logic used by `web_app.py`.

### `main`

```python
def main():
```

This function runs the plot-only program.

Matplotlib is imported inside the function:

```python
import matplotlib.pyplot as plt
```

That means matplotlib is only loaded when the plot-only program actually runs.

The function loads the compound list:

```python
compounds = load_compound_list()
```

Then it gets PubChem data:

```python
found_compounds, skipped_compounds = get_many_compounds(compounds)
```

The skipped compounds are printed:

```python
for compound in skipped_compounds:
    print("Skipping:", compound)
```

The program also prints how many compounds will be plotted.

If there are no found compounds, the function stops early:

```python
if len(found_compounds) == 0:
    print("No compounds to plot.")
    return
```

Then it builds two lists:

- `tpsas` for the x-axis
- `xlogps` for the y-axis

The matplotlib commands create and show the plot:

```python
plt.figure(figsize=(12, 8))
plt.scatter(tpsas, xlogps)
```

The next loop adds compound names next to the points.

The final lines label the axes, add a title, and show the plot window:

```python
plt.xlabel(...)
plt.ylabel(...)
plt.title(...)
plt.show()
```

### Main Guard

```python
if __name__ == "__main__":
    main()
```

This means the plot runs only when this file is started directly:

```text
python pubchem_amp.py
```

## `test_pubchem_amp.py`

This file tests the business logic and the plot-only program.

The tests use fake PubChem responses, so they do not need internet access.

### Imports

```python
import requests
import compound_logic
import pubchem_amp
from compound_logic import get_compound_names, get_many_compounds, get_pubchem_data
```

- `requests` is used so the test can raise `requests.RequestException`.
- `compound_logic` lets the test compare imported functions.
- `pubchem_amp` is the plot-only program being tested.
- The direct imports make the tests shorter to write.

### `FakeResponse`

```python
class FakeResponse:
```

This class acts like a small fake version of a real `requests` response.

The constructor stores fake JSON data:

```python
def __init__(self, data):
    self.data = data
```

`raise_for_status` does nothing because the fake response is pretending the
request succeeded:

```python
def raise_for_status(self):
    pass
```

`json` returns the fake data:

```python
def json(self):
    return self.data
```

### `test_plot_program_uses_day08_business_logic`

This test checks that `pubchem_amp.py` uses `get_many_compounds` from
`compound_logic.py`.

It helps prove the plot-only program and the web app share the same day 8
business logic.

### `test_get_compound_names_splits_text_into_names`

This test checks that typed text is split correctly.

It confirms that both new lines and commas can separate compound names.

### `test_get_pubchem_data_returns_tpsa_and_xlogp`

This test creates a fake PubChem response with both required values:

- `TPSA`
- `XLogP`

It passes a fake request function into `get_pubchem_data`, then checks that the
returned dictionary has the expected name and numbers.

### `test_get_pubchem_data_returns_none_when_data_is_missing`

This test gives fake data that has `TPSA` but does not have `XLogP`.

The correct result is `None`, because the program needs both values.

### `test_get_pubchem_data_returns_none_when_request_fails`

This test makes the fake request raise `requests.RequestException`.

The correct result is `None`, because a failed web request means the compound
cannot be used.

### `test_get_many_compounds_returns_found_and_skipped_lists`

This test sends two compound names:

- `octanol`
- `missing`

The fake request returns complete data for `octanol` and incomplete data for
`missing`.

The test checks that:

- `octanol` goes into the found list
- `missing` goes into the skipped list

## `test_web_app.py`

This file tests the FastAPI web app.

### Imports

```python
from fastapi.testclient import TestClient

import compound_logic
import web_app
```

- `TestClient` lets pytest call the FastAPI app without opening a real browser.
- `compound_logic` is used to check that the web app imports the correct
  business logic.
- `web_app` is the app being tested.

### `client`

```python
client = TestClient(web_app.app)
```

This creates a fake browser/client for testing the FastAPI app.

### `test_web_app_uses_day08_business_logic`

This test checks that `web_app.py` uses `get_many_compounds` from
`compound_logic.py`.

### `test_home_page_renders_form`

This test asks the app for `/`, the home page:

```python
response = client.get("/")
```

It checks that:

- the response status is `200`, meaning success
- the page contains `PubChem Amphiphile App`
- the page contains `Choose compounds:`

This proves the form page can render.

### `test_search_page_uses_business_logic_and_shows_results`

This test checks the submitted form behavior.

It creates a dictionary called `calls` so the test can remember what names were
sent into the business logic.

Then it defines a fake `get_many_compounds` function:

```python
def fake_get_many_compounds(names):
```

The fake function:

- stores the names it received
- returns one fake found compound
- returns no skipped compounds

The `monkeypatch` line temporarily replaces the real PubChem lookup:

```python
monkeypatch.setattr(web_app, "get_many_compounds", fake_get_many_compounds)
```

That means the test does not use the internet.

Then the test sends a fake form request:

```python
response = client.get("/", params={...})
```

The test checks that:

- selected and typed names became `["decanol", "octanol"]`
- the response status is `200`
- the page says `Found 1 compounds.`
- the page contains `octanol`

## How The Files Work Together

When you run the web app:

1. `web_app.py` starts FastAPI.
2. The browser asks for `/`.
3. `home` returns the HTML form.
4. The browser asks for `/styles.css`.
5. `styles` returns the CSS file.
6. The user submits compounds.
7. `home` calls `choose_compound_names`.
8. `home` calls `get_many_compounds`.
9. `get_many_compounds` calls `get_pubchem_data`.
10. `make_page` builds the results table.
11. `plot_logic.make_plot_svg` builds the browser plot.
12. The browser shows the final page.

When you run the tests:

1. pytest imports the test files.
2. the tests use fake data instead of real PubChem requests.
3. the tests check that the business logic, plot-only program, and web app work
   as expected.
