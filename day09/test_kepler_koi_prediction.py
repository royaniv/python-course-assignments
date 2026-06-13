import kepler_koi_prediction


CSV_HEADER = (
    "kepoi_name,koi_disposition,koi_period,koi_duration,koi_depth,koi_impact,"
    "koi_prad,koi_steff,koi_srad,koi_slogg,koi_kepmag"
)


def make_sample(features, label):
    return {
        "name": "test koi",
        "features": features,
        "label": label,
    }


def test_make_data_url_uses_nasa_kepler_koi_table():
    data_url = kepler_koi_prediction.make_data_url()

    assert data_url.startswith("https://exoplanetarchive.ipac.caltech.edu/TAP/sync")
    assert "cumulative" in data_url
    assert "koi_disposition" in data_url
    assert "format=csv" in data_url


def test_load_data_reads_confirmed_and_false_positive_rows(tmp_path):
    data_path = tmp_path / "kepler_koi.csv"
    data_path.write_text(
        "\n".join(
            [
                CSV_HEADER,
                "K00001.01,CONFIRMED,10,3,500,0.1,1.0,5700,1.0,4.4,12",
                "K00002.01,FALSE POSITIVE,1,6,20000,0.9,12.0,6100,1.4,4.1,14",
                "K00003.01,CANDIDATE,20,4,600,0.2,1.1,5400,0.9,4.5,13",
            ]
        ),
        encoding="utf-8",
    )

    samples = kepler_koi_prediction.load_data(data_path)

    assert len(samples) == 2
    assert samples[0]["name"] == "K00001.01"
    assert samples[0]["features"][0] == 10
    assert samples[0]["label"] == "CONFIRMED"
    assert samples[1]["label"] == "FALSE POSITIVE"


def test_train_model_predicts_nearest_kind_of_koi():
    train_samples = [
        make_sample([10, 3, 500, 0.1, 1.0, 5700, 1.0, 4.4, 12], "CONFIRMED"),
        make_sample([11, 3, 550, 0.2, 1.1, 5650, 1.0, 4.5, 12], "CONFIRMED"),
        make_sample([1, 6, 20000, 0.9, 12.0, 6100, 1.4, 4.1, 14], "FALSE POSITIVE"),
        make_sample([2, 7, 21000, 0.8, 13.0, 6200, 1.5, 4.0, 14], "FALSE POSITIVE"),
    ]
    model = kepler_koi_prediction.train_model(train_samples, n_neighbors=1)

    prediction = model.predict([[10.5, 3.1, 525, 0.1, 1.0, 5680, 1.0, 4.4, 12]])

    assert prediction[0] == "CONFIRMED"


def test_evaluate_model_returns_predictions():
    samples = [
        make_sample([10, 3, 500, 0.1, 1.0, 5700, 1.0, 4.4, 12], "CONFIRMED"),
        make_sample([11, 3, 550, 0.2, 1.1, 5650, 1.0, 4.5, 12], "CONFIRMED"),
        make_sample([12, 3, 600, 0.1, 1.0, 5750, 1.0, 4.4, 12], "CONFIRMED"),
        make_sample([1, 6, 20000, 0.9, 12.0, 6100, 1.4, 4.1, 14], "FALSE POSITIVE"),
        make_sample([2, 7, 21000, 0.8, 13.0, 6200, 1.5, 4.0, 14], "FALSE POSITIVE"),
        make_sample([3, 6, 19000, 0.9, 11.0, 6050, 1.3, 4.1, 14], "FALSE POSITIVE"),
    ]

    train_samples, test_samples, accuracy, prediction_rows = (
        kepler_koi_prediction.evaluate_model(
            samples,
            test_fraction=0.33,
            seed=9,
            n_neighbors=1,
        )
    )

    assert len(train_samples) == 4
    assert len(test_samples) == 2
    assert 0 <= accuracy <= 1
    assert len(prediction_rows) == 2
    assert {"name", "actual", "predicted", "correct"} == set(prediction_rows[0])
