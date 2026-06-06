import requests
import matplotlib.pyplot as plt

compounds = [
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

valid_compounds = []
tpsas = []
xlogps = []

for compound in compounds:

    print("Looking up:", compound)

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound}/property/XLogP,TPSA/JSON"

    response = requests.get(url)

    data = response.json()

    properties = data["PropertyTable"]["Properties"][0]

    if "TPSA" in properties and "XLogP" in properties:

        valid_compounds.append(compound)

        tpsas.append(properties["TPSA"])

        xlogps.append(properties["XLogP"])

    else:

        print("Skipping:", compound)

print("Number of compounds plotted:", len(valid_compounds))

plt.figure(figsize=(12, 8))

plt.scatter(tpsas, xlogps)

for number in range(len(valid_compounds)):

    plt.text(
        tpsas[number] + 1,
        xlogps[number] + 0.1,
        valid_compounds[number]
    )

plt.xlim(min(tpsas) - 5, max(tpsas) + 15)
plt.ylim(min(xlogps) - 1, max(xlogps) + 1)

plt.xlabel("TPSA")
plt.ylabel("XLogP")
plt.title("Amphiphiles from PubChem")

plt.show()