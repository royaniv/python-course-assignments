from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from compound_logic import DEFAULT_COMPOUNDS, get_compound_names, get_many_compounds


app = FastAPI()


def make_page(compound_text=None, found_compounds=None, skipped_compounds=None):
    if compound_text is None:
        compound_text = "\n".join(DEFAULT_COMPOUNDS)

    result_html = ""

    if found_compounds is not None:
        rows = ""

        for compound in found_compounds:
            rows += f"""
            <tr>
                <td>{compound["name"]}</td>
                <td>{compound["tpsa"]}</td>
                <td>{compound["xlogp"]}</td>
            </tr>
            """

        skipped_text = ", ".join(skipped_compounds)

        result_html = f"""
        <h2>Results</h2>
        <p>Found {len(found_compounds)} compounds.</p>
        <table>
            <tr>
                <th>Compound</th>
                <th>TPSA</th>
                <th>XLogP</th>
            </tr>
            {rows}
        </table>
        <p><strong>Skipped:</strong> {skipped_text}</p>
        """

    return f"""
    <!doctype html>
    <html>
    <head>
        <title>PubChem Amphiphile App</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                max-width: 800px;
            }}

            textarea {{
                width: 100%;
                height: 220px;
            }}

            button {{
                margin-top: 10px;
                padding: 8px 14px;
            }}

            table {{
                border-collapse: collapse;
                margin-top: 15px;
                width: 100%;
            }}

            th, td {{
                border: 1px solid #cccccc;
                padding: 8px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <h1>PubChem Amphiphile App</h1>

        <form method="get">
            <p>Enter compound names, one per line:</p>
            <textarea name="compound_text">{compound_text}</textarea>
            <br>
            <button type="submit">Look up compounds</button>
        </form>

        {result_html}
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home(compound_text=None):
    if compound_text is None:
        return make_page()

    compound_names = get_compound_names(compound_text)
    found_compounds, skipped_compounds = get_many_compounds(compound_names)

    return make_page(compound_text, found_compounds, skipped_compounds)


@app.get("/api/compounds")
def api_compounds(names=None):
    compound_names = get_compound_names(names)
    found_compounds, skipped_compounds = get_many_compounds(compound_names)

    return {
        "found": found_compounds,
        "skipped": skipped_compounds,
    }
