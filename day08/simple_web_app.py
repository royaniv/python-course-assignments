import sys
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

COURSE_ROOT = Path(__file__).resolve().parents[1]
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))

import plot_logic
from day06.compound_logic import choose_compound_names, get_many_compounds, load_compound_list


STYLE_PATH = Path(__file__).with_name("styles.css")


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


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            query = parse_qs(parsed.query)
            if "submitted" not in query:
                page = make_page()
            else:
                names = choose_compound_names(query.get("selected_compounds", []), query.get("compound_text", [""])[0])
                found, skipped = get_many_compounds(names)
                page = make_page(query.get("compound_text", [""])[0], query.get("selected_compounds", []), found, skipped)
            self.send_text(page, "text/html; charset=utf-8")
            return

        if parsed.path == "/styles.css":
            self.send_text(STYLE_PATH.read_text(encoding="utf-8"), "text/css; charset=utf-8")
            return

        self.send_error(404)

    def send_text(self, text, content_type):
        data = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def make_page_from_query(query_string):
    query = parse_qs(query_string)

    if "submitted" not in query:
        return make_page()

    compound_text = query.get("compound_text", [""])[0]
    selected_compounds = query.get("selected_compounds", [])
    names = choose_compound_names(selected_compounds, compound_text)
    found, skipped = get_many_compounds(names)

    return make_page(compound_text, selected_compounds, found, skipped)


def run_server(port=8000):
    print(f"Starting simple web app at http://127.0.0.1:{port}/")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    run_server()
