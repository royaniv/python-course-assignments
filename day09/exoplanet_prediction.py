import csv
import math
import random
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlretrieve


TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
QUERY = """
select pl_name,hostname,pl_orbper,pl_rade,st_teff,st_rad,st_mass,pl_eqt
from pscomppars
where pl_orbper is not null
and pl_rade is not null
and st_teff is not null
and st_rad is not null
and st_mass is not null
and pl_eqt is not null
"""
DATA_PATH = Path(__file__).with_name("data") / "exoplanets.csv"
REPORT_PATH = Path(__file__).with_name("results") / "prediction_report.txt"
FEATURE_NAMES = [
    "orbital period in days",
    "planet radius in Earth radii",
    "stellar effective temperature in K",
    "stellar radius in Solar radii",
    "stellar mass in Solar masses",
]


def make_data_url():
    query = " ".join(QUERY.split())
    arguments = urlencode({"query": query, "format": "csv"})
    return TAP_URL + "?" + arguments


def download_data(data_path=DATA_PATH):
    data_path.parent.mkdir(exist_ok=True)
    urlretrieve(make_data_url(), data_path)
    return data_path


def temperature_label(equilibrium_temperature):
    if 180 <= equilibrium_temperature <= 310:
        return "temperate"

    return "not_temperate"


def load_data(data_path=DATA_PATH):
    if not data_path.exists():
        download_data(data_path)

    samples = []

    with data_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            try:
                measurements = [
                    float(row["pl_orbper"]),
                    float(row["pl_rade"]),
                    float(row["st_teff"]),
                    float(row["st_rad"]),
                    float(row["st_mass"]),
                ]
                equilibrium_temperature = float(row["pl_eqt"])
            except (KeyError, TypeError, ValueError):
                continue

            samples.append(
                {
                    "planet": row["pl_name"],
                    "host": row["hostname"],
                    "measurements": measurements,
                    "equilibrium_temperature": equilibrium_temperature,
                    "label": temperature_label(equilibrium_temperature),
                }
            )

    return samples


def split_data(samples, test_fraction=0.30, seed=9):
    shuffled_samples = samples.copy()
    random.Random(seed).shuffle(shuffled_samples)

    test_count = int(len(shuffled_samples) * test_fraction)
    test_samples = shuffled_samples[:test_count]
    train_samples = shuffled_samples[test_count:]

    return train_samples, test_samples


def make_feature_ranges(train_samples):
    feature_count = len(train_samples[0]["measurements"])
    ranges = []

    for index in range(feature_count):
        values = [sample["measurements"][index] for sample in train_samples]
        smallest = min(values)
        largest = max(values)
        ranges.append((smallest, largest))

    return ranges


def scale_measurements(measurements, feature_ranges):
    scaled = []

    for value, (smallest, largest) in zip(measurements, feature_ranges):
        value_range = largest - smallest

        if value_range == 0:
            scaled.append(0)
        else:
            scaled.append((value - smallest) / value_range)

    return scaled


def distance(first_measurements, second_measurements):
    total = 0

    for first, second in zip(first_measurements, second_measurements):
        total += (first - second) ** 2

    return math.sqrt(total)


def predict_label(train_samples, measurements, feature_ranges, k=5):
    scaled_measurements = scale_measurements(measurements, feature_ranges)

    neighbors = sorted(
        train_samples,
        key=lambda sample: distance(
            scale_measurements(sample["measurements"], feature_ranges),
            scaled_measurements,
        ),
    )
    nearest_labels = [sample["label"] for sample in neighbors[:k]]
    votes = Counter(nearest_labels)

    return votes.most_common(1)[0][0]


def evaluate_model(train_samples, test_samples, k=5):
    correct = 0
    prediction_rows = []
    feature_ranges = make_feature_ranges(train_samples)

    for sample in test_samples:
        predicted_label = predict_label(
            train_samples,
            sample["measurements"],
            feature_ranges,
            k,
        )
        is_correct = predicted_label == sample["label"]

        if is_correct:
            correct += 1

        prediction_rows.append(
            {
                "planet": sample["planet"],
                "host": sample["host"],
                "equilibrium_temperature": sample["equilibrium_temperature"],
                "actual": sample["label"],
                "predicted": predicted_label,
                "correct": is_correct,
            }
        )

    accuracy = correct / len(test_samples)
    return accuracy, prediction_rows


def label_counts(samples):
    return Counter(sample["label"] for sample in samples)


def make_report(samples, train_samples, test_samples, accuracy, prediction_rows):
    lines = [
        "Exoplanet Temperateness Prediction",
        "",
        f"Dataset rows: {len(samples)}",
        f"Training rows: {len(train_samples)}",
        f"Testing rows: {len(test_samples)}",
        f"Accuracy: {accuracy:.1%}",
        "",
        "Target labels:",
    ]

    for label, count in sorted(label_counts(samples).items()):
        lines.append(f"- {label}: {count}")

    lines.extend(
        [
            "",
            "The model predicts whether an exoplanet is temperate from:",
        ]
    )

    for feature_name in FEATURE_NAMES:
        lines.append(f"- {feature_name}")

    lines.extend(
        [
            "",
            "A planet is labelled temperate if its equilibrium temperature is",
            "between 180 K and 310 K.",
            "",
            "First 10 test predictions:",
        ]
    )

    for row in prediction_rows[:10]:
        status = "correct" if row["correct"] else "wrong"
        lines.append(
            f"- {row['planet']} around {row['host']}: predicted {row['predicted']}; "
            f"actual {row['actual']}; Teq {row['equilibrium_temperature']:.0f} K "
            f"({status})"
        )

    return "\n".join(lines)


def save_report(report, report_path=REPORT_PATH):
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(report, encoding="utf-8")


def main():
    samples = load_data()
    train_samples, test_samples = split_data(samples)
    accuracy, prediction_rows = evaluate_model(train_samples, test_samples)
    report = make_report(samples, train_samples, test_samples, accuracy, prediction_rows)

    save_report(report)
    print(report)
    print()
    print(f"Saved report to {REPORT_PATH}")


if __name__ == "__main__":
    main()
