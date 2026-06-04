import requests
import pandas as pd
import matplotlib.pyplot as plt

compounds = [
    "octanol",
    "nonanol",
    "decanol",
    "undecanol",
    "dodecanol",
    "tridecanol",
    "tetradecanol",
    "pentadecanol",
    "cetyl alcohol",
    "stearyl alcohol",

    "octylamine",
    "nonylamine",
    "decylamine",
    "undecylamine",
    "dodecylamine",
    "tridecylamine",
    "tetradecylamine",
    "pentadecylamine",
    "cetylamine",
    "stearylamine"
]

results = []

for compound in compounds:

    url = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        f"{compound}/property/"
        f"MolecularWeight,XLogP,TPSA/JSON"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Could not find {compound}")
        continue

    data = response.json()

    try:
        p = data["PropertyTable"]["Properties"][0]

        results.append({
            "Compound": compound,
            "MolecularWeight": p.get("MolecularWeight"),
            "XLogP": p.get("XLogP"),
            "TPSA": p.get("TPSA")
        })

    except Exception:
        print(f"Problem reading {compound}")

df = pd.DataFrame(results)

print(df)

plt.scatter(df["TPSA"], df["XLogP"])

plt.xlabel("TPSA")
plt.ylabel("XLogP")
plt.title("Amphiphile Properties from PubChem")

plt.show()