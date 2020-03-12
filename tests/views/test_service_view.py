import asynctest
from asynctest import mock
from starlette.testclient import TestClient

from authal.main import app

client = TestClient(app)


@asynctest.mock.patch("authal.domain.get_version_from_cat_api")
def test_cat_api_example_view(mock_domain_get_version_from_cat_api: mock.Mock):
    mock_domain_get_version_from_cat_api.return_value = {"version": "6.6.6"}

    response = client.get("/services/cat-api")

    expected_response = {"authal": {"version": "0.0.1"}, "cat-api": {"version": "6.6.6"}}
    assert (response.status_code, response.json()) == (200, expected_response)
