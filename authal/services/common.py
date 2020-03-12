import httpx

from authal import config


# DEMO: setting an httpx async client with h2 support enabled and informative user-agent
class ServiceClient(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        kwargs["http2"] = True

        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"].update({"User-Agent": f"Authal/{config.VERSION}"})

        super().__init__(*args, **kwargs)
