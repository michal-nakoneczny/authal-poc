from starlette.testclient import TestClient

from authal.main import app

client = TestClient(app)


# DEMO: talk about why testing views DOES NOT need to be done in an async test case
def test_root_view():
    response = client.get("/", allow_redirects=False)

    assert (response.status_code, response.headers["location"]) == (303, "/docs")
