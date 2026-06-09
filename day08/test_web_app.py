from fastapi.testclient import TestClient

import web_app


client = TestClient(web_app.app)


def test_home_page_loads():
    response = client.get("/")

    assert response.status_code == 200
    assert "PubChem Amphiphile App" in response.text
    assert "textarea" in response.text


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
