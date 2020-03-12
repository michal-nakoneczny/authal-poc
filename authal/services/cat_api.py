from typing import Any, List, Union

from authal import dto
from authal.services.common import ServiceClient


# DEMO: communicating with an external service using httpx in an async function
async def get_version() -> Union[dto.JSON, List[Any]]:
    async with ServiceClient() as client:
        response = await client.get("https://cat.gengo.com/api/status")

    return response.json()
