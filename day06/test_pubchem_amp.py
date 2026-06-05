import requests

def test_octanol_values_are_positive():

    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/octanol/property/XLogP,TPSA/JSON"

    response = requests.get(url)

    data = response.json()

    properties = data["PropertyTable"]["Properties"][0]

    assert properties["TPSA"] > 0
    assert properties["XLogP"] > 0