from urllib.parse import quote

import requests


DEFAULT_COMPOUNDS = [
    "octanol",
    "decanol",
    "dodecanol",
    "tetradecanol",
    "cetyl alcohol",
    "octylamine",
    "decylamine",
    "dodecylamine",
    "tetradecylamine",
    "cetylamine",
    "octanoic acid",
    "decanoic acid",
    "dodecanoic acid",
    "tetradecanoic acid",
    "oleyl alcohol",
    "oleylamine",
    "sodium dodecyl sulfate",
]


def get_compound_names(text):
    if text is None or text.strip() == "":
        return DEFAULT_COMPOUNDS

    text = text.replace(",", "\n")
    names = []

    for line in text.splitlines():
        name = line.strip()

        if name != "":
            names.append(name)

    return names


def get_pubchem_data(compound, requests_get=requests.get):
    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        + quote(compound)
        + "/property/XLogP,TPSA/JSON"
    )

    try:
        response = requests_get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        properties = data["PropertyTable"]["Properties"][0]

        if "TPSA" in properties and "XLogP" in properties:
            return {
                "name": compound,
                "tpsa": float(properties["TPSA"]),
                "xlogp": float(properties["XLogP"]),
            }
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        return None

    return None


def get_many_compounds(compounds, requests_get=requests.get):
    found_compounds = []
    skipped_compounds = []

    for compound in compounds:
        result = get_pubchem_data(compound, requests_get)

        if result is None:
            skipped_compounds.append(compound)
        else:
            found_compounds.append(result)

    return found_compounds, skipped_compounds
