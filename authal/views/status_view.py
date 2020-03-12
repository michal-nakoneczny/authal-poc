from fastapi import APIRouter

from authal import config, dto

router = APIRouter()


# DEMO: an async view that does not communicate with anything but should be async because of how
# FastAPI handles path operations
@router.get("/status", operation_id="status_view", response_model=dto.StatusViewResponse)
async def status_view() -> dto.JSON:
    """
    Status view returning the name and version of this service and a link to Swagger documentation.

    \f
    :return:
    """
    return {
        "service": "authal",
        "version": config.VERSION,
        "links": [{"href": "/docs", "rel": "documentation", "type": "GET"}],
    }
