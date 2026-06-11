from fastapi.testclient import TestClient

import day06.compound_logic as day06_logic
import web_app


client = TestClient(web_app.app)


def test_web_app_uses_day06_business_logic():
    assert web_app.get_many_compounds is day06_logic.get_many_compounds


def test_home_page_renders_form():
    response = client.get("/")

    assert response.status_code == 200
    assert "PubChem Amphiphile App" in response.text
    assert "Choose compounds:" in response.text


def test_search_page_uses_business_logic_and_shows_results(monkeypatch):
    calls = {}

    def fake_get_many_compounds(names):
        calls["names"] = names
        return [{"name": "octanol", "tpsa": 20.2, "xlogp": 2.9}], []

    monkeypatch.setattr(web_app, "get_many_compounds", fake_get_many_compounds)

    response = client.get(
        "/",
        params={
            "submitted": "yes",
            "selected_compounds": "decanol",
            "compound_text": "octanol",
        },
    )

    assert calls["names"] == ["decanol", "octanol"]
    assert response.status_code == 200
    assert "Found 1 compounds." in response.text
    assert "octanol" in response.text
