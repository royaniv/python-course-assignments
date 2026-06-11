import web_app


def test_home_page_renders_form():
    page = web_app.make_page()

    assert "PubChem Amphiphile App" in page
    assert "Choose compounds:" in page


def test_search_page_uses_business_logic_and_shows_results(monkeypatch):
    calls = {}

    def fake_get_many_compounds(names):
        calls["names"] = names
        return [{"name": "octanol", "tpsa": 20.2, "xlogp": 2.9}], []

    monkeypatch.setattr(web_app, "get_many_compounds", fake_get_many_compounds)

    page = web_app.make_page_from_query(
        "submitted=yes&selected_compounds=decanol&compound_text=octanol"
    )

    assert calls["names"] == ["decanol", "octanol"]
    assert "Found 1 compounds." in page
    assert "octanol" in page
