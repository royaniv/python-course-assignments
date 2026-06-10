from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from compound_logic import get_compound_names, get_many_compounds, load_compound_list


def choose_compound_names(selected_compounds=None, compound_text=""):
    names = []

    if selected_compounds is not None:
        for compound in selected_compounds:
            compound = compound.strip()

            if compound != "":
                names.append(compound)

    names.extend(get_compound_names(compound_text))

    unique_names = []

    for name in names:
        if name not in unique_names:
            unique_names.append(name)

    return unique_names


def make_plot_svg(found_compounds):
    if len(found_compounds) == 0:
        return ""

    tpsas = []
    xlogps = []

    for compound in found_compounds:
        tpsas.append(compound["tpsa"])
        xlogps.append(compound["xlogp"])

    min_tpsa = min(tpsas)
    max_tpsa = max(tpsas)
    min_xlogp = min(xlogps)
    max_xlogp = max(xlogps)

    if min_tpsa == max_tpsa:
        min_tpsa -= 1
        max_tpsa += 1

    if min_xlogp == max_xlogp:
        min_xlogp -= 1
        max_xlogp += 1

    width = 720
    height = 430
    left = 85
    right = 30
    top = 40
    bottom = 75
    plot_width = width - left - right
    plot_height = height - top - bottom

    points = ""
    labels = ""

    for compound in found_compounds:
        x = left + (compound["tpsa"] - min_tpsa) / (max_tpsa - min_tpsa) * plot_width
        y = top + (max_xlogp - compound["xlogp"]) / (max_xlogp - min_xlogp) * plot_height

        points += f'<circle class="plot-point" cx="{x:.1f}" cy="{y:.1f}" r="5"></circle>\n'
        labels += (
            f'<text class="plot-label" x="{x + 8:.1f}" y="{y - 8:.1f}">'
            f'{escape(compound["name"])}</text>\n'
        )

    x_axis_y = height - bottom

    return f"""
    <div class="plot-box">
        <h3>Plot</h3>
        <svg class="plot-svg" viewBox="0 0 {width} {height}" role="img" aria-label="Scatter plot of TPSA and XLogP values">
            <line class="plot-axis" x1="{left}" y1="{x_axis_y}" x2="{width - right}" y2="{x_axis_y}"></line>
            <line class="plot-axis" x1="{left}" y1="{top}" x2="{left}" y2="{x_axis_y}"></line>

            <text class="plot-tick" x="{left}" y="{x_axis_y + 22}">{min_tpsa:.1f}</text>
            <text class="plot-tick" x="{width - right}" y="{x_axis_y + 22}" text-anchor="end">{max_tpsa:.1f}</text>
            <text class="plot-tick" x="{left - 12}" y="{x_axis_y}" text-anchor="end">{min_xlogp:.1f}</text>
            <text class="plot-tick" x="{left - 12}" y="{top + 4}" text-anchor="end">{max_xlogp:.1f}</text>

            {points}
            {labels}

            <text class="plot-axis-label" x="{left + plot_width / 2:.1f}" y="{height - 22}" text-anchor="middle">TPSA (topological polar surface area)</text>
            <text class="plot-axis-label" transform="translate(24 {top + plot_height / 2:.1f}) rotate(-90)" text-anchor="middle">XLogP (octanol-water partition coefficient)</text>
        </svg>
    </div>
    """


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

    skipped_text = ""

    if skipped_compounds:
        skipped_text = ", ".join(skipped_compounds)

    if skipped_text == "":
        skipped_text = "None"

    plot_html = make_plot_svg(found_compounds)

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

        {plot_html}
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
        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                background: #f4f1e8;
                color: #1f2933;
                font-family: Arial, sans-serif;
                line-height: 1.5;
                margin: 0;
            }}

            .page {{
                margin: 0 auto;
                max-width: 980px;
                padding: 32px 24px 48px;
            }}

            header {{
                background: #163b40;
                border-bottom: 6px solid #d17a45;
                color: white;
                padding: 34px 24px;
            }}

            header h1 {{
                font-size: 34px;
                line-height: 1.1;
                margin: 0;
            }}

            header p {{
                color: #d7e5df;
                font-size: 17px;
                margin: 12px 0 0;
                max-width: 680px;
            }}

            .search-panel, .results {{
                background: #ffffff;
                border: 1px solid #d8d6ca;
                border-radius: 8px;
                box-shadow: 0 12px 28px rgba(31, 41, 51, 0.08);
                margin-top: 24px;
                padding: 24px;
            }}

            .form-grid {{
                display: grid;
                gap: 22px;
                grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            }}

            label {{
                display: block;
                font-weight: bold;
                margin-bottom: 8px;
            }}

            select, textarea {{
                border: 1px solid #b8c3bd;
                border-radius: 6px;
                color: #1f2933;
                font: inherit;
                width: 100%;
            }}

            select {{
                min-height: 220px;
                padding: 10px;
            }}

            textarea {{
                min-height: 220px;
                padding: 12px;
                resize: vertical;
            }}

            select:focus, textarea:focus {{
                border-color: #2b7a78;
                box-shadow: 0 0 0 3px rgba(43, 122, 120, 0.18);
                outline: none;
            }}

            button {{
                background: #2b7a78;
                border: 0;
                border-radius: 6px;
                color: white;
                cursor: pointer;
                font: inherit;
                font-weight: bold;
                margin-top: 18px;
                padding: 11px 18px;
            }}

            button:hover {{
                background: #245f60;
            }}

            .section-heading {{
                align-items: center;
                display: flex;
                justify-content: space-between;
                gap: 16px;
                margin-bottom: 14px;
            }}

            .section-heading h2 {{
                margin: 0;
            }}

            .section-heading span {{
                background: #f3d9c8;
                border-radius: 999px;
                color: #6d381f;
                font-weight: bold;
                padding: 5px 10px;
                white-space: nowrap;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            th {{
                background: #e6eee9;
                color: #163b40;
            }}

            th, td {{
                border-bottom: 1px solid #d8d6ca;
                padding: 11px 10px;
                text-align: left;
            }}

            tr:nth-child(even) td {{
                background: #fbfaf6;
            }}

            small {{
                color: #52616b;
                font-weight: normal;
            }}

            .skipped {{
                color: #52616b;
                margin-bottom: 0;
            }}

            .plot-box {{
                margin-top: 24px;
            }}

            .plot-box h3 {{
                margin: 0 0 12px;
            }}

            .plot-svg {{
                background: #fbfaf6;
                border: 1px solid #d8d6ca;
                border-radius: 6px;
                display: block;
                height: auto;
                max-width: 100%;
            }}

            .plot-axis {{
                stroke: #52616b;
                stroke-width: 2;
            }}

            .plot-point {{
                fill: #2b7a78;
                stroke: white;
                stroke-width: 2;
            }}

            .plot-label, .plot-tick {{
                fill: #1f2933;
                font-size: 12px;
            }}

            .plot-axis-label {{
                fill: #163b40;
                font-size: 14px;
                font-weight: bold;
            }}

            @media (max-width: 700px) {{
                .page {{
                    padding: 20px 14px 36px;
                }}

                header {{
                    padding: 28px 16px;
                }}

                header h1 {{
                    font-size: 28px;
                }}

                .form-grid {{
                    grid-template-columns: 1fr;
                }}

                .search-panel, .results {{
                    padding: 18px;
                }}

                .section-heading {{
                    align-items: flex-start;
                    flex-direction: column;
                }}
            }}
        </style>
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
    submitted = "submitted" in query

    if not submitted:
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

        if parsed_url.path != "/":
            self.send_error(404)
            return

        page = make_page_from_query(parsed_url.query)
        page_bytes = page.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page_bytes)))
        self.end_headers()
        self.wfile.write(page_bytes)


def run_server(port=8000):
    server = HTTPServer(("127.0.0.1", port), AmphiphileHandler)
    print("Open http://127.0.0.1:" + str(port))
    server.serve_forever()


if __name__ == "__main__":
    run_server()
