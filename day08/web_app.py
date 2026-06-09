from html import escape
from io import BytesIO
from urllib.parse import urlencode

import matplotlib

matplotlib.use("Agg")

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, StreamingResponse

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


def make_plot_png(selected_compounds=None, compound_text=None):
    compound_names = get_web_compound_names(selected_compounds, compound_text)
    found_compounds, _skipped_compounds = get_many_compounds(compound_names)

    import matplotlib.pyplot as plt

    figure, axis = plt.subplots(figsize=(6, 4))

    if found_compounds:
        tpsas = [compound["tpsa"] for compound in found_compounds]
        xlogps = [compound["xlogp"] for compound in found_compounds]

        axis.scatter(tpsas, xlogps, color="royalblue")

        for compound in found_compounds:
            axis.annotate(
                compound["name"],
                (compound["tpsa"], compound["xlogp"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8,
            )

        axis.set_xlabel("TPSA")
        axis.set_ylabel("XLogP")
        axis.set_title("Amphiphile properties")
    else:
        axis.text(
            0.5,
            0.5,
            "No compounds found yet\nTry the search form",
            ha="center",
            va="center",
            fontsize=10,
        )
        axis.set_axis_off()

    figure.tight_layout()

    buffer = BytesIO()
    figure.savefig(buffer, format="png")
    plt.close(figure)

    return buffer.getvalue()


def make_page(
    compound_text="",
    selected_compounds=None,
    found_compounds=None,
    skipped_compounds=None,
):
    if selected_compounds is None:
        selected_compounds = DEFAULT_COMPOUNDS

    datalist_options = "".join(
        f'<option value="{escape(compound, quote=True)}"></option>'
        for compound in DEFAULT_COMPOUNDS
    )

    result_html = ""
    plot_html = ""

    plot_params = urlencode(
        {
            "compound_text": compound_text,
            "selected_compounds": selected_compounds,
        },
        doseq=True,
    )
    plot_html = f'<h2>Plot</h2><img src="/plot?{plot_params}" alt="Plot of amphiphile properties" style="max-width: 100%;">'

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

            <p>Type or choose compounds from the long dropdown list:</p>
            <input
                type="text"
                name="compound_text"
                value="{escape(compound_text)}"
                list="compound-suggestions"
                placeholder="octanol, decanol, oleic acid"
                style="width: 100%; padding: 8px; box-sizing: border-box;"
            >
            <datalist id="compound-suggestions">
                {datalist_options}
            </datalist>
            <br>
            <button type="submit">Look up compounds</button>
        </form>

        {result_html}
        {plot_html}
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


@app.get("/plot")
def plot(compound_text=None, selected_compounds: list[str] | None = Query(default=None)):
    if selected_compounds is None:
        selected_compounds = []

    plot_bytes = make_plot_png(selected_compounds, compound_text)

    return StreamingResponse(iter([plot_bytes]), media_type="image/png")


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
