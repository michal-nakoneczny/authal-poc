from starlette.testclient import TestClient

from authal import config
from authal.main import app

client = TestClient(app)


def test_status_view():
    response = client.get("/status")
    assert (response.status_code, response.json()) == (
        200,
        {
            "service": "authal",
            "version": config.VERSION,
            "links": [{"href": "/docs", "rel": "documentation", "type": "GET"}],
        },
    )
