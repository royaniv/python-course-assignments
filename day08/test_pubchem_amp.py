import sys
from pathlib import Path

import requests

import pubchem_amp

COURSE_ROOT = Path(__file__).resolve().parents[1]
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))

import day06.compound_logic as day06_logic
from day06.compound_logic import get_compound_names, get_many_compounds, get_pubchem_data


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_plot_program_uses_day06_business_logic():
    assert pubchem_amp.get_many_compounds is day06_logic.get_many_compounds


def test_get_compound_names_splits_text_into_names():
    text = "octanol\ndecanol, dodecanol"

    names = get_compound_names(text)

    assert names == ["octanol", "decanol", "dodecanol"]


def test_get_pubchem_data_returns_tpsa_and_xlogp():
    def fake_get(url, timeout):
        data = {
            "PropertyTable": {
                "Properties": [
                    {
                        "TPSA": 20.2,
                        "XLogP": 2.9,
                    }
                ]
            }
        }

        return FakeResponse(data)

    result = get_pubchem_data("octanol", fake_get)

    assert result == {
        "name": "octanol",
        "tpsa": 20.2,
        "xlogp": 2.9,
    }


def test_get_pubchem_data_returns_none_when_data_is_missing():
    def fake_get(url, timeout):
        data = {
            "PropertyTable": {
                "Properties": [
                    {
                        "TPSA": 20.2,
                    }
                ]
            }
        }

        return FakeResponse(data)

    result = get_pubchem_data("octanol", fake_get)

    assert result is None


def test_get_pubchem_data_returns_none_when_request_fails():
    def fake_get(url, timeout):
        raise requests.RequestException()

    result = get_pubchem_data("octanol", fake_get)

    assert result is None


def test_get_many_compounds_returns_found_and_skipped_lists():
    def fake_get(url, timeout):
        if "missing" in url:
            data = {"PropertyTable": {"Properties": [{"TPSA": 20.2}]}}
        else:
            data = {
                "PropertyTable": {
                    "Properties": [
                        {
                            "TPSA": 20.2,
                            "XLogP": 2.9,
                        }
                    ]
                }
            }

        return FakeResponse(data)

    found, skipped = get_many_compounds(["octanol", "missing"], fake_get)

    assert found == [
        {
            "name": "octanol",
            "tpsa": 20.2,
            "xlogp": 2.9,
        }
    ]
    assert skipped == ["missing"]
