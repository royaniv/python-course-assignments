import requests

compound = "octanol"

url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound}/property/XLogP,TPSA/JSON"

response = requests.get(url)

data = response.json()

properties = data["PropertyTable"]["Properties"][0]

print("Testing", compound)

if "TPSA" in properties and "XLogP" in properties:
    print("PASS")
else:
    print("FAIL")