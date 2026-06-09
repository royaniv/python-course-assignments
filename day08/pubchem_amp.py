import matplotlib.pyplot as plt

from compound_logic import DEFAULT_COMPOUNDS, get_many_compounds


def main():
    found_compounds, skipped_compounds = get_many_compounds(DEFAULT_COMPOUNDS)

    for compound in skipped_compounds:
        print("Skipping:", compound)

    print("Number of compounds plotted:", len(found_compounds))

    if len(found_compounds) == 0:
        print("No compounds to plot.")
        return

    tpsas = []
    xlogps = []

    for compound in found_compounds:
        tpsas.append(compound["tpsa"])
        xlogps.append(compound["xlogp"])

    plt.figure(figsize=(12, 8))
    plt.scatter(tpsas, xlogps)

    for compound in found_compounds:
        plt.text(
            compound["tpsa"] + 1,
            compound["xlogp"] + 0.1,
            compound["name"],
        )

    plt.xlabel("TPSA")
    plt.ylabel("XLogP")
    plt.title("Amphiphiles from PubChem")
    plt.show()


if __name__ == "__main__":
    main()
