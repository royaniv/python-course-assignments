from fastapi.testclient import TestClient

import web_app


client = TestClient(web_app.app)


def test_home_page_loads():
    response = client.get("/")

    assert response.status_code == 200
    assert "PubChem Amphiphile App" in response.text
    assert 'name="selected_compounds"' in response.text
    assert 'name="compound_text"' in response.text


def test_api_suggestions_uses_pubchem(monkeypatch):
    def fake_get(url, timeout=10):
        assert "autocomplete/compound/etha" in url
        return type("Resp", (), {"json": lambda self: {"dictionary_terms": {"compound": ["ethanol"]}}, "raise_for_status": lambda self: None})()

    monkeypatch.setattr(web_app, "get_pubchem_suggestions", lambda query: ["ethanol"])

    response = client.get("/api/suggestions", params={"query": "etha"})

    assert response.status_code == 200
    assert response.json() == ["ethanol"]


def test_api_compounds_uses_business_logic(monkeypatch):
    def fake_get_many_compounds(compound_names):
        assert compound_names == ["octanol", "missing"]

        return (
            [
                {
                    "name": "octanol",
                    "tpsa": 20.2,
                    "xlogp": 2.9,
                }
            ],
            ["missing"],
        )

    monkeypatch.setattr(web_app, "get_many_compounds", fake_get_many_compounds)

    response = client.get("/api/compounds", params={"names": "octanol\nmissing"})

    assert response.status_code == 200
    assert response.json() == {
        "found": [
            {
                "name": "octanol",
                "tpsa": 20.2,
                "xlogp": 2.9,
            }
        ],
        "skipped": ["missing"],
    }


def test_web_page_shows_results(monkeypatch):
    def fake_get_many_compounds(compound_names):
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

    response = client.get("/", params={"compound_text": "octanol"})

    assert response.status_code == 200
    assert "Found 1 compounds" in response.text
    assert "octanol" in response.text


def test_web_page_includes_plot_link(monkeypatch):
    def fake_get_many_compounds(compound_names):
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

    response = client.get("/", params={"compound_text": "octanol"})

    assert response.status_code == 200
    assert 'src="/plot?compound_text=octanol"' in response.text


def test_plot_endpoint_returns_png(monkeypatch):
    def fake_get_many_compounds(compound_names):
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

    response = client.get("/plot", params={"compound_text": "octanol"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/png")


def test_web_page_uses_selected_and_extra_compounds(monkeypatch):
    def fake_get_many_compounds(compound_names):
        assert compound_names == ["octanol", "decanol", "oleic acid"]

        return ([], [])

    monkeypatch.setattr(web_app, "get_many_compounds", fake_get_many_compounds)

    response = client.get(
        "/",
        params=[
            ("submitted", "yes"),
            ("selected_compounds", "octanol"),
            ("selected_compounds", "decanol"),
            ("compound_text", "oleic acid"),
        ],
    )

    assert response.status_code == 200
    assert "Found 0 compounds" in response.text
