import csv
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlretrieve

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
FEATURE_COLUMNS = [
    "koi_period",
    "koi_duration",
    "koi_depth",
    "koi_impact",
    "koi_prad",
    "koi_steff",
    "koi_srad",
    "koi_slogg",
    "koi_kepmag",
]
FEATURE_NAMES = [
    "orbital period in days",
    "transit duration in hours",
    "transit depth in parts per million",
    "impact parameter",
    "estimated planet radius in Earth radii",
    "stellar effective temperature in K",
    "stellar radius in Solar radii",
    "stellar surface gravity",
    "Kepler-band magnitude",
]
TARGET_LABELS = {"CONFIRMED", "FALSE POSITIVE"}
QUERY = f"""
select kepoi_name,koi_disposition,{",".join(FEATURE_COLUMNS)}
from cumulative
where koi_disposition in ('CONFIRMED','FALSE POSITIVE')
and {" is not null and ".join(FEATURE_COLUMNS)} is not null
"""
DATA_PATH = Path(__file__).with_name("data") / "kepler_koi.csv"
REPORT_PATH = Path(__file__).with_name("results") / "prediction_report.txt"


def make_data_url():
    query = " ".join(QUERY.split())
    arguments = urlencode({"query": query, "format": "csv"})
    return TAP_URL + "?" + arguments


def download_data(data_path=DATA_PATH):
    data_path.parent.mkdir(exist_ok=True)
    urlretrieve(make_data_url(), data_path)
    return data_path


def load_data(data_path=DATA_PATH):
    if not data_path.exists():
        download_data(data_path)

    samples = []

    with data_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            label = row.get("koi_disposition", "").strip()

            if label not in TARGET_LABELS:
                continue

            try:
                features = [float(row[column]) for column in FEATURE_COLUMNS]
            except (KeyError, TypeError, ValueError):
                continue

            samples.append(
                {
                    "name": row["kepoi_name"],
                    "features": features,
                    "label": label,
                }
            )

    return samples


def split_samples(samples, test_fraction=0.30, seed=9):
    labels = [sample["label"] for sample in samples]
    label_counts = Counter(labels)
    stratify_labels = labels if min(label_counts.values()) > 1 else None

    return train_test_split(
        samples,
        test_size=test_fraction,
        random_state=seed,
        stratify=stratify_labels,
    )


def make_model(n_neighbors=5):
    return make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=n_neighbors),
    )


def train_model(train_samples, n_neighbors=5):
    neighbor_count = min(n_neighbors, len(train_samples))
    model = make_model(neighbor_count)
    features = [sample["features"] for sample in train_samples]
    labels = [sample["label"] for sample in train_samples]

    model.fit(features, labels)
    return model


def evaluate_model(samples, test_fraction=0.30, seed=9, n_neighbors=5):
    train_samples, test_samples = split_samples(samples, test_fraction, seed)
    model = train_model(train_samples, n_neighbors)
    test_features = [sample["features"] for sample in test_samples]
    actual_labels = [sample["label"] for sample in test_samples]
    predicted_labels = model.predict(test_features)
    accuracy = accuracy_score(actual_labels, predicted_labels)
    prediction_rows = []

    for sample, predicted_label in zip(test_samples, predicted_labels):
        prediction_rows.append(
            {
                "name": sample["name"],
                "actual": sample["label"],
                "predicted": predicted_label,
                "correct": predicted_label == sample["label"],
            }
        )

    return train_samples, test_samples, accuracy, prediction_rows


def label_counts(samples):
    return Counter(sample["label"] for sample in samples)


def make_report(samples, train_samples, test_samples, accuracy, prediction_rows):
    lines = [
        "Kepler KOI Planet Classification",
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
            "The model predicts the Exoplanet Archive disposition from:",
        ]
    )

    for feature_name in FEATURE_NAMES:
        lines.append(f"- {feature_name}")

    lines.extend(["", "First 10 test predictions:"])

    for row in prediction_rows[:10]:
        status = "correct" if row["correct"] else "wrong"
        lines.append(
            f"- {row['name']}: predicted {row['predicted']}; "
            f"actual {row['actual']} ({status})"
        )

    return "\n".join(lines)


def save_report(report, report_path=REPORT_PATH):
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(report, encoding="utf-8")


def main():
    samples = load_data()
    train_samples, test_samples, accuracy, prediction_rows = evaluate_model(samples)
    report = make_report(samples, train_samples, test_samples, accuracy, prediction_rows)

    save_report(report)
    print(report)
    print()
    print(f"Saved report to {REPORT_PATH}")


if __name__ == "__main__":
    main()
