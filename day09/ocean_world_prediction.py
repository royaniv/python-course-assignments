import csv
import math
import random
from collections import Counter
from pathlib import Path


DATA_PATH = Path(__file__).with_name("data") / "ocean_worlds.csv"
REPORT_PATH = Path(__file__).with_name("results") / "prediction_report.txt"
FEATURE_NAMES = [
    "radius in km",
    "density in g/cm3",
    "surface temperature in K",
    "activity score",
]


def load_data(data_path=DATA_PATH):
    samples = []

    with data_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            try:
                measurements = [
                    float(row["radius_km"]),
                    float(row["density_g_cm3"]),
                    float(row["surface_temp_k"]),
                    float(row["activity_score"]),
                ]
            except (KeyError, TypeError, ValueError):
                continue

            samples.append(
                {
                    "world": row["world"],
                    "location": row["location"],
                    "measurements": measurements,
                    "label": row["ocean_evidence"],
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
        ranges.append((min(values), max(values)))

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


def predict_label(train_samples, measurements, feature_ranges, k=3):
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


def evaluate_model(train_samples, test_samples, k=3):
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
                "world": sample["world"],
                "location": sample["location"],
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
        "Ocean World Evidence Prediction",
        "",
        f"Dataset rows: {len(samples)}",
        f"Training rows: {len(train_samples)}",
        f"Testing rows: {len(test_samples)}",
        f"Accuracy: {accuracy:.1%}",
        "",
        "Labels:",
    ]

    for label, count in sorted(label_counts(samples).items()):
        lines.append(f"- {label}: {count}")

    lines.extend(
        [
            "",
            "The model predicts the evidence label from:",
        ]
    )

    for feature_name in FEATURE_NAMES:
        lines.append(f"- {feature_name}")

    lines.extend(["", "Test predictions:"])

    for row in prediction_rows:
        status = "correct" if row["correct"] else "wrong"
        lines.append(
            f"- {row['world']} ({row['location']}): predicted {row['predicted']}; "
            f"actual {row['actual']} ({status})"
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
