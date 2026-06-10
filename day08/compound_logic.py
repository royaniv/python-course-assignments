from pathlib import Path
from urllib.parse import quote

import requests


def load_compound_list(path="compound_list.txt"):
    file_path = Path(__file__).with_name(path)

    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as handle:
            names = [line.strip() for line in handle if line.strip()]

        if names:
            return names

    return []


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
