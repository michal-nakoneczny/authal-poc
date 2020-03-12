import asyncio

import pytest


@pytest.yield_fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# DEMO: this shows how to block actual requests (sync and async) from httpx while also providing
# a helpful message to the developer.
@pytest.fixture(autouse=True)
def prevent_actual_requests(monkeypatch):
    def mock_request(*args, **kwargs):
        raise Exception(
            "Executing actual remote requests is not permitted in tests. "
            "See authal.tests.conftest.prevent_actual_requests for more information."
        )

    async def mock_async_request(*args, **kwargs):
        raise Exception(
            "Executing actual remote requests is not permitted in tests. "
            "See authal.tests.conftest.prevent_actual_requests for more information."
        )

    monkeypatch.setattr("httpx.Client.request", mock_request)
    monkeypatch.setattr("httpx.AsyncClient.request", mock_async_request)
