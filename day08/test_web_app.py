import sys
from pathlib import Path

import web_app

COURSE_ROOT = Path(__file__).resolve().parents[1]
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))

import day06.compound_logic as day06_logic
from day06.compound_logic import choose_compound_names


def test_web_app_uses_day06_business_logic():
    assert web_app.get_many_compounds is day06_logic.get_many_compounds


def test_choose_compound_names_combines_list_and_text():
    names = choose_compound_names(
        ["octanol", "decanol"],
        "oleic acid, octanol",
    )

    assert names == ["octanol", "decanol", "oleic acid"]


def test_home_page_has_form():
    html = web_app.make_page()

    assert "PubChem Amphiphile App" in html
    assert 'name="selected_compounds"' in html
    assert 'name="compound_text"' in html


def test_results_page_shows_compounds_and_explanations():
    found_compounds = [
        {
            "name": "octanol",
            "tpsa": 20.2,
            "xlogp": 2.9,
        }
    ]

    html = web_app.make_page(
        compound_text="octanol",
        found_compounds=found_compounds,
        skipped_compounds=["missing"],
    )

    assert "Found 1 compounds" in html
    assert "octanol" in html
    assert "topological polar surface area" in html
    assert "octanol-water partition coefficient" in html
    assert "missing" in html
    assert "<svg" in html


def test_page_from_query_uses_business_logic(monkeypatch):
    def fake_get_many_compounds(compound_names):
        assert compound_names == ["octanol", "decanol", "oleic acid"]

        return (
            [
                {
                    "name": "octanol",
                    "tpsa": 20.2,
                    "xlogp": 2.9,
                }
            ],
            [],
        )

    monkeypatch.setattr(web_app, "get_many_compounds", fake_get_many_compounds)

    html = web_app.make_page_from_query(
        "submitted=yes&selected_compounds=octanol"
        "&selected_compounds=decanol&compound_text=oleic+acid"
    )

    assert "Found 1 compounds" in html
    assert "octanol" in html
    assert "<svg" in html
