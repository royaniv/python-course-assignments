import ocean_world_prediction


def make_sample(measurements, label="strong_evidence"):
    return {
        "world": "test world",
        "location": "test location",
        "measurements": measurements,
        "label": label,
    }


def test_load_data_reads_included_ocean_worlds():
    samples = ocean_world_prediction.load_data()

    names = [sample["world"] for sample in samples]

    assert "Europa" in names
    assert "Enceladus" in names
    assert "Ceres" in names


def test_distance_between_same_measurements_is_zero():
    result = ocean_world_prediction.distance([1, 2, 3], [1, 2, 3])

    assert result == 0


def test_predict_label_uses_nearest_neighbors():
    train_samples = [
        make_sample([1.0, 1.0], "strong_evidence"),
        make_sample([1.1, 1.0], "strong_evidence"),
        make_sample([9.0, 9.0], "possible_evidence"),
        make_sample([9.1, 9.0], "possible_evidence"),
    ]
    feature_ranges = ocean_world_prediction.make_feature_ranges(train_samples)

    prediction = ocean_world_prediction.predict_label(
        train_samples,
        [1.2, 1.0],
        feature_ranges,
        k=3,
    )

    assert prediction == "strong_evidence"


def test_evaluate_model_calculates_accuracy():
    train_samples = [
        make_sample([1.0, 1.0], "strong_evidence"),
        make_sample([9.0, 9.0], "possible_evidence"),
    ]
    test_samples = [
        make_sample([1.1, 1.0], "strong_evidence"),
        make_sample([8.9, 9.0], "possible_evidence"),
    ]

    accuracy, prediction_rows = ocean_world_prediction.evaluate_model(
        train_samples,
        test_samples,
        k=1,
    )

    assert accuracy == 1
    assert prediction_rows[0]["predicted"] == "strong_evidence"
    assert prediction_rows[1]["predicted"] == "possible_evidence"
