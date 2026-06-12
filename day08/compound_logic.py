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


def load_compound_list():
    return DEFAULT_COMPOUNDS.copy()


def get_compound_names(text):
    if text is None:
        return []

    text = text.replace(",", "\n")
    names = []

    for line in text.splitlines():
        name = line.strip()

        if name != "":
            names.append(name)

    return names


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


def get_many_compounds(compound_names, requests_get=requests.get):
    found_compounds = []
    skipped_compounds = []

    for compound in compound_names:
        result = get_pubchem_data(compound, requests_get)

        if result is None:
            skipped_compounds.append(compound)
        else:
            found_compounds.append(result)

    return found_compounds, skipped_compounds
