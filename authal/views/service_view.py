from fastapi import APIRouter

from authal import config, domain, dto

router = APIRouter()


# DEMO: async view getting data from an external service through the domain
@router.get("/services/cat-api", operation_id="cat_api_example_view")
async def cat_api_example_view() -> dto.JSON:
    cat_api_version = await domain.get_version_from_cat_api()
    return {"authal": {"version": config.VERSION}, "cat-api": cat_api_version}
