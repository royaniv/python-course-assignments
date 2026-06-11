import sys
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

COURSE_ROOT = Path(__file__).resolve().parents[1]
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))

from day06.compound_logic import choose_compound_names, get_many_compounds, load_compound_list


STYLE_PATH = Path(__file__).with_name("styles.css")

PLOT_WIDTH = 720
PLOT_HEIGHT = 430
PLOT_LEFT = 85
PLOT_RIGHT = 30
PLOT_TOP = 40
PLOT_BOTTOM = 75


def make_compound_options(selected_compounds=None):
    if selected_compounds is None:
        selected_compounds = []

    selected_names = set(selected_compounds)
    options = ""

    for compound in load_compound_list():
        selected = " selected" if compound in selected_names else ""
        options += (
            f'<option value="{escape(compound, quote=True)}"{selected}>'
            f"{escape(compound)}</option>\n"
        )

    return options


def make_plot_svg(found_compounds):
    if len(found_compounds) == 0:
        return ""

    tpsas = [compound["tpsa"] for compound in found_compounds]
    xlogps = [compound["xlogp"] for compound in found_compounds]

    min_tpsa = min(tpsas)
    max_tpsa = max(tpsas)
    min_xlogp = min(xlogps)
    max_xlogp = max(xlogps)

    tpsa_range = max(max_tpsa - min_tpsa, 1)
    xlogp_range = max(max_xlogp - min_xlogp, 1)
    min_tpsa -= tpsa_range * 0.1
    max_tpsa += tpsa_range * 0.1
    min_xlogp -= xlogp_range * 0.1
    max_xlogp += xlogp_range * 0.1

    plot_width = PLOT_WIDTH - PLOT_LEFT - PLOT_RIGHT
    plot_height = PLOT_HEIGHT - PLOT_TOP - PLOT_BOTTOM
    x_axis_y = PLOT_HEIGHT - PLOT_BOTTOM
    points = ""

    for compound in found_compounds:
        x = PLOT_LEFT + (compound["tpsa"] - min_tpsa) / (max_tpsa - min_tpsa) * plot_width
        y = PLOT_TOP + (max_xlogp - compound["xlogp"]) / (max_xlogp - min_xlogp) * plot_height
        name = escape(compound["name"])

        points += (
            f'<circle class="plot-point" cx="{x:.1f}" cy="{y:.1f}" r="5">'
            f"<title>{name}</title></circle>\n"
        )

    return f"""
    <div class="plot-box">
        <h3>Plot</h3>
        <svg class="plot-svg" viewBox="0 0 {PLOT_WIDTH} {PLOT_HEIGHT}" role="img" aria-label="Scatter plot of TPSA and XLogP values">
            <line class="plot-axis" x1="{PLOT_LEFT}" y1="{x_axis_y}" x2="{PLOT_WIDTH - PLOT_RIGHT}" y2="{x_axis_y}"></line>
            <line class="plot-axis" x1="{PLOT_LEFT}" y1="{PLOT_TOP}" x2="{PLOT_LEFT}" y2="{x_axis_y}"></line>

            <text class="plot-tick" x="{PLOT_LEFT}" y="{x_axis_y + 22}">{min_tpsa:.1f}</text>
            <text class="plot-tick" x="{PLOT_WIDTH - PLOT_RIGHT}" y="{x_axis_y + 22}" text-anchor="end">{max_tpsa:.1f}</text>
            <text class="plot-tick" x="{PLOT_LEFT - 12}" y="{x_axis_y}" text-anchor="end">{min_xlogp:.1f}</text>
            <text class="plot-tick" x="{PLOT_LEFT - 12}" y="{PLOT_TOP + 4}" text-anchor="end">{max_xlogp:.1f}</text>

            {points}

            <text class="plot-axis-label" x="{PLOT_LEFT + plot_width / 2:.1f}" y="{PLOT_HEIGHT - 22}" text-anchor="middle">TPSA (topological polar surface area)</text>
            <text class="plot-axis-label" transform="translate(24 {PLOT_TOP + plot_height / 2:.1f}) rotate(-90)" text-anchor="middle">XLogP (octanol-water partition coefficient)</text>
        </svg>
    </div>
    """


def make_results_html(found_compounds=None, skipped_compounds=None):
    if found_compounds is None:
        return ""

    rows = ""

    for compound in found_compounds:
        rows += f"""
        <tr>
            <td>{escape(compound["name"])}</td>
            <td>{compound["tpsa"]}</td>
            <td>{compound["xlogp"]}</td>
        </tr>
        """

    skipped_text = "None"

    if skipped_compounds:
        skipped_text = ", ".join(skipped_compounds)

    return f"""
    <section class="results">
        <div class="section-heading">
            <h2>Results</h2>
            <span>{len(found_compounds)} found</span>
        </div>

        <p class="result-count">Found {len(found_compounds)} compounds.</p>
        <table>
            <tr>
                <th>Compound</th>
                <th>TPSA<br><small>topological polar surface area</small></th>
                <th>XLogP<br><small>octanol-water partition coefficient</small></th>
            </tr>
            {rows}
        </table>
        <p class="skipped"><strong>Skipped:</strong> {escape(skipped_text)}</p>
        {make_plot_svg(found_compounds)}
    </section>
    """


def make_page(
    compound_text="",
    selected_compounds=None,
    found_compounds=None,
    skipped_compounds=None,
):
    compound_options = make_compound_options(selected_compounds)
    results_html = make_results_html(found_compounds, skipped_compounds)

    return f"""
    <!doctype html>
    <html>
    <head>
        <title>PubChem Amphiphile App</title>
        <link rel="stylesheet" href="/styles.css">
    </head>
    <body>
        <header>
            <div class="page">
                <h1>PubChem Amphiphile App</h1>
                <p>Look up amphiphile compounds and compare TPSA with XLogP.</p>
            </div>
        </header>

        <main class="page">
            <section class="search-panel">
                <form method="get">
                    <input type="hidden" name="submitted" value="yes">

                    <div class="form-grid">
                        <div>
                            <label for="selected_compounds">Choose compounds from the list</label>
                            <select id="selected_compounds" name="selected_compounds" multiple size="8">
                                {compound_options}
                            </select>
                        </div>

                        <div>
                            <label for="compound_text">Type other PubChem compound names</label>
                            <textarea id="compound_text" name="compound_text" placeholder="octanol&#10;decanol&#10;oleic acid">{escape(compound_text)}</textarea>
                        </div>
                    </div>

                    <button type="submit">Look up compounds</button>
                </form>
            </section>

            {results_html}
        </main>
    </body>
    </html>
    """


def make_page_from_query(query_string):
    query = parse_qs(query_string)

    if "submitted" not in query:
        return make_page()

    compound_text = query.get("compound_text", [""])[0]
    selected_compounds = query.get("selected_compounds", [])
    compound_names = choose_compound_names(selected_compounds, compound_text)
    found_compounds, skipped_compounds = get_many_compounds(compound_names)

    return make_page(
        compound_text,
        selected_compounds,
        found_compounds,
        skipped_compounds,
    )


class AmphiphileHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/":
            page = make_page_from_query(parsed_url.query)
            self.send_text(page, "text/html; charset=utf-8")
            return

        if parsed_url.path == "/styles.css":
            css = STYLE_PATH.read_text(encoding="utf-8")
            self.send_text(css, "text/css; charset=utf-8")
            return

        self.send_error(404)

    def send_text(self, text, content_type):
        text_bytes = text.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(text_bytes)))
        self.end_headers()
        self.wfile.write(text_bytes)


def run_server(port=8000):
    server = HTTPServer(("127.0.0.1", port), AmphiphileHandler)
    print("Open http://127.0.0.1:" + str(port))
    server.serve_forever()


if __name__ == "__main__":
    run_server()
