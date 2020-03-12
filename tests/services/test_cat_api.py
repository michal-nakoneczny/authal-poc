import asynctest
import pytest
from asynctest import mock
from starlette.testclient import TestClient

from authal.main import app
from authal.services import cat_api

client = TestClient(app)


# DEMO: talk about mocking in async test cases
@asynctest.mock.patch("authal.services.common.ServiceClient.get")
@pytest.mark.asyncio
async def test_get_version(mock_service_client_get: mock.Mock):
    mock_service_client_get.return_value = mock.Mock(
        status_code=200, json=lambda: {"version": "6.6.6"}
    )

    result = await cat_api.get_version()

    expected_result = {"version": "6.6.6"}
    assert result == expected_result
    mock_service_client_get.assert_called_once_with("https://cat.gengo.com/api/status")
