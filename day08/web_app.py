from html import escape

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from compound_logic import DEFAULT_COMPOUNDS, get_compound_names, get_many_compounds


app = FastAPI()


def get_web_compound_names(selected_compounds=None, compound_text=None):
    names = []

    if selected_compounds is not None:
        names.extend(selected_compounds)

    if compound_text is not None and compound_text.strip() != "":
        names.extend(get_compound_names(compound_text))

    unique_names = []

    for name in names:
        name = name.strip()

        if name != "" and name not in unique_names:
            unique_names.append(name)

    return unique_names


def make_page(
    compound_text="",
    selected_compounds=None,
    found_compounds=None,
    skipped_compounds=None,
):
    if selected_compounds is None:
        selected_compounds = DEFAULT_COMPOUNDS

    selected_names = set(selected_compounds)
    checkbox_html = ""

    for compound in DEFAULT_COMPOUNDS:
        checked = ""

        if compound in selected_names:
            checked = " checked"

        checkbox_html += f"""
        <label class="compound-option">
            <input
                type="checkbox"
                name="selected_compounds"
                value="{escape(compound, quote=True)}"
                {checked}
            >
            <span>{escape(compound)}</span>
        </label>
        """

    result_html = ""

    if found_compounds is not None:
        rows = ""

        for compound in found_compounds:
            rows += f"""
            <tr>
                <td>{escape(compound["name"])}</td>
                <td>{compound["tpsa"]}</td>
                <td>{compound["xlogp"]}</td>
            </tr>
            """

        skipped_text = escape(", ".join(skipped_compounds))

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

            .compound-list {{
                display: grid;
                gap: 8px;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                margin-bottom: 20px;
            }}

            .compound-option {{
                align-items: center;
                display: flex;
                gap: 8px;
            }}

            textarea {{
                width: 100%;
                height: 120px;
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
            <input type="hidden" name="submitted" value="yes">

            <p>Choose compounds from the starter list:</p>
            <div class="compound-list">
                {checkbox_html}
            </div>

            <p>Add other compound names, one per line:</p>
            <textarea name="compound_text">{escape(compound_text)}</textarea>
            <br>
            <button type="submit">Look up compounds</button>
        </form>

        {result_html}
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home(
    compound_text=None,
    selected_compounds: list[str] | None = Query(default=None),
    submitted=None,
):
    if compound_text is None and selected_compounds is None and submitted is None:
        return make_page()

    if selected_compounds is None:
        selected_compounds = []

    compound_names = get_web_compound_names(selected_compounds, compound_text)
    found_compounds, skipped_compounds = get_many_compounds(compound_names)

    return make_page(compound_text or "", selected_compounds, found_compounds, skipped_compounds)


@app.get("/api/compounds")
def api_compounds(names=None):
    compound_names = get_compound_names(names)
    found_compounds, skipped_compounds = get_many_compounds(compound_names)

    return {
        "found": found_compounds,
        "skipped": skipped_compounds,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
