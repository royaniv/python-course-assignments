import requests

from compound_logic import (
    get_compound_names,
    get_pubchem_data,
)


class FakeResponse:

    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_split_names():

    names = get_compound_names(
        "octanol\ndecanol,dodecanol"
    )

    assert names == [
        "octanol",
        "decanol",
        "dodecanol",
    ]


def test_pubchem_success():

    def fake_get(url, timeout):

        return FakeResponse({
            "PropertyTable": {
                "Properties": [
                    {
                        "TPSA": 20.2,
                        "XLogP": 2.9,
                    }
                ]
            }
        })

    result = get_pubchem_data(
        "octanol",
        fake_get,
    )

    assert result["name"] == "octanol"
    assert result["tpsa"] == 20.2
    assert result["xlogp"] == 2.9


def test_missing_property():

    def fake_get(url, timeout):

        return FakeResponse({
            "PropertyTable": {
                "Properties": [
                    {
                        "TPSA": 20.2
                    }
                ]
            }
        })

    result = get_pubchem_data(
        "octanol",
        fake_get,
    )

    assert result is None


def test_request_failure():

    def fake_get(url, timeout):
        raise requests.RequestException()

    result = get_pubchem_data(
        "octanol",
        fake_get,
    )

    assert result is None