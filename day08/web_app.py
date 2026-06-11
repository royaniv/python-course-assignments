"""Compatibility wrapper for the simplified Day 8 app."""

from simple_web_app import Handler, make_page, make_page_from_query, run_server

__all__ = ["Handler", "make_page", "make_page_from_query", "run_server"]

if __name__ == "__main__":
    run_server()
