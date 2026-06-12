import exoplanet_prediction


def make_sample(measurements, label="temperate"):
    return {
        "planet": "test planet",
        "host": "test star",
        "measurements": measurements,
        "equilibrium_temperature": 250,
        "label": label,
    }


def test_temperature_label_marks_temperate_range():
    assert exoplanet_prediction.temperature_label(250) == "temperate"
    assert exoplanet_prediction.temperature_label(500) == "not_temperate"


def test_distance_between_same_measurements_is_zero():
    result = exoplanet_prediction.distance([1, 2, 3], [1, 2, 3])

    assert result == 0


def test_predict_label_uses_nearest_neighbors():
    train_samples = [
        make_sample([1.0, 1.0], "temperate"),
        make_sample([1.1, 1.0], "temperate"),
        make_sample([9.0, 9.0], "not_temperate"),
        make_sample([9.1, 9.0], "not_temperate"),
    ]
    feature_ranges = exoplanet_prediction.make_feature_ranges(train_samples)

    prediction = exoplanet_prediction.predict_label(
        train_samples,
        [1.2, 1.0],
        feature_ranges,
        k=3,
    )

    assert prediction == "temperate"


def test_evaluate_model_calculates_accuracy():
    train_samples = [
        make_sample([1.0, 1.0], "temperate"),
        make_sample([9.0, 9.0], "not_temperate"),
    ]
    test_samples = [
        make_sample([1.1, 1.0], "temperate"),
        make_sample([8.9, 9.0], "not_temperate"),
    ]

    accuracy, prediction_rows = exoplanet_prediction.evaluate_model(
        train_samples,
        test_samples,
        k=1,
    )

    assert accuracy == 1
    assert prediction_rows[0]["predicted"] == "temperate"
    assert prediction_rows[1]["predicted"] == "not_temperate"
