import sys
from html import escape
from pathlib import Path
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

COURSE_ROOT = Path(__file__).resolve().parents[1]
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))

import plot_logic
from day06.compound_logic import choose_compound_names, get_many_compounds, load_compound_list


STYLE_PATH = Path(__file__).with_name("styles.css")
app = FastAPI()


def make_page(compound_text="", selected_compounds=None, found_compounds=None, skipped_compounds=None):
    selected_names = set(selected_compounds or [])
    options = ""

    for name in load_compound_list():
        chosen = " selected" if name in selected_names else ""
        options += f'<option value="{escape(name, quote=True)}"{chosen}>{escape(name)}</option>\n'

    rows = "".join(
        f"<tr><td>{escape(c['name'])}</td><td>{c['tpsa']}</td><td>{c['xlogp']}</td></tr>"
        for c in (found_compounds or [])
    )

    skipped_text = ", ".join(skipped_compounds) if skipped_compounds else "None"

    return f"""
    <!doctype html>
    <html>
    <head><title>Simple PubChem App</title><link rel="stylesheet" href="/styles.css"></head>
    <body>
      <h1>PubChem Amphiphile App</h1>
      <form method="get">
        <input type="hidden" name="submitted" value="yes">
        <p>Choose compounds:</p>
        <select name="selected_compounds" multiple size="6">{options}</select>
        <p>Or type names:</p>
        <textarea name="compound_text">{escape(compound_text)}</textarea>
        <p><button type="submit">Search</button></p>
      </form>
      <h2>Results</h2>
      <p>Found {len(found_compounds or [])} compounds.</p>
      <table>
        <tr>
          <th>Compound</th>
          <th>TPSA<br><small>topological polar surface area</small></th>
          <th>XLogP<br><small>octanol-water partition coefficient</small></th>
        </tr>
        {rows}
      </table>
      {plot_logic.make_plot_svg(found_compounds or [])}
      <p>Skipped: {escape(skipped_text)}</p>
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home(
    submitted: Optional[str] = None,
    compound_text: str = "",
    selected_compounds: Optional[List[str]] = Query(default=None),
):
    if submitted is None:
        return make_page()

    selected_compounds = selected_compounds or []
    names = choose_compound_names(selected_compounds, compound_text)
    found, skipped = get_many_compounds(names)
    return make_page(compound_text, selected_compounds, found, skipped)


@app.get("/styles.css", response_class=PlainTextResponse)
def styles():
    return PlainTextResponse(STYLE_PATH.read_text(encoding="utf-8"), media_type="text/css")


def run_server(port=8001):
    print(f"Starting FastAPI web app at http://127.0.0.1:{port}/")
    uvicorn.run(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    run_server()
