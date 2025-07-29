"""Tests for the Flask web interface."""

from src.web_app import create_app


def test_create_app() -> None:
    """Ensure the Flask app can be created."""

    app = create_app(api_key="test")
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

    # TODO: add more tests for /ask endpoint
