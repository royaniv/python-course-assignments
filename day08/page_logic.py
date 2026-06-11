import sys
from html import escape
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parents[1]
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))

import plot_logic
from day06.compound_logic import choose_compound_names, get_many_compounds, load_compound_list


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

    rows = "".join(
        f"""
        <tr>
            <td>{escape(compound['name'])}</td>
            <td>{compound['tpsa']}</td>
            <td>{compound['xlogp']}</td>
        </tr>
        """
        for compound in found_compounds
    )

    skipped_text = ", ".join(skipped_compounds) if skipped_compounds else "None"

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
        {plot_logic.make_plot_svg(found_compounds)}
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
    from urllib.parse import parse_qs

    query = parse_qs(query_string)

    if "submitted" not in query:
        return make_page()

    compound_text = query.get("compound_text", [""])[0]
    selected_compounds = query.get("selected_compounds", [])
    compound_names = choose_compound_names(selected_compounds, compound_text)
    found_compounds, skipped_compounds = get_many_compounds(compound_names)

    return make_page(compound_text, selected_compounds, found_compounds, skipped_compounds)
