import requests
import matplotlib.pyplot as plt

compounds = [
    "octanol",
    "octylamine",
    "octanoic acid",
    "dodecanol",
    "dodecylamine",
    "dodecanoic acid",
    "cetyl alcohol",
    "cetylamine"
]

tpsas = []
xlogps = []

for compound in compounds:

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound}/property/XLogP,TPSA/JSON"

    response = requests.get(url)

    data = response.json()

    properties = data["PropertyTable"]["Properties"][0]

    tpsas.append(properties["TPSA"])
    xlogps.append(properties["XLogP"])

print("Compound\tTPSA\tXLogP")

for compound, tpsa, xlogp in zip(compounds, tpsas, xlogps):

    print(compound, "\t", tpsa, "\t", xlogp)

plt.scatter(tpsas, xlogps)

for compound, tpsa, xlogp in zip(compounds, tpsas, xlogps):

    plt.text(
        tpsa + 1,
        xlogp + 0.1,
        compound
    )

plt.xlabel("TPSA")
plt.ylabel("XLogP")
plt.title("Amphiphiles from PubChem")

plt.show()