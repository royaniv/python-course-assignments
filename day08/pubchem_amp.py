import sys
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parents[1]
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))

from day06.compound_logic import get_many_compounds, load_compound_list


def main():
    import matplotlib.pyplot as plt

    compounds = load_compound_list()
    found_compounds, skipped_compounds = get_many_compounds(compounds)

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

    plt.xlabel("TPSA (topological polar surface area)")
    plt.ylabel("XLogP (octanol-water partition coefficient)")
    plt.title("Amphiphiles from PubChem")
    plt.show()


if __name__ == "__main__":
    main()
