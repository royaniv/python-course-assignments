from fastapi.testclient import TestClient

import web_app

client = TestClient(web_app.app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200
    assert "PubChem Amphiphile App" in response.text


def test_search_page(monkeypatch):

    def fake_get_many_compounds(names):

        return [
            {
                "name": "octanol",
                "tpsa": 20.2,
                "xlogp": 2.9,
            }
        ], []

    monkeypatch.setattr(
        web_app,
        "get_many_compounds",
        fake_get_many_compounds,
    )

    response = client.get(
        "/",
        params={
            "submitted": "yes",
            "compound_text": "octanol",
        },
    )

    assert response.status_code == 200
    assert "octanol" in response.text