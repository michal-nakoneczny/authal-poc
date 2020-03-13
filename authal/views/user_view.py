import logging
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query

from authal import config, domain, dto

router = APIRouter()
logger = logging.getLogger(__name__)


# DEMO: show request body handling and validation, response serialization, non-standard response
# status code
@router.post("/users", status_code=HTTPStatus.CREATED)
async def create_user(unsaved_user: dto.UnsavedUser) -> dto.JSON:
    """
    Create view for creating a new User given an UnsavedUser payload.

    \f
    :return:
    """
    user = await domain.create_user(unsaved_user)
    return user.dict()


# DEMO: show very verbose documentation around optional and default query params and response
# schema
@router.get("/users", response_model=dto.UserSummaryPaginatedResponse)
async def list_users(
    limit: int = Query(
        config.DEFAULT_PAGE_LIMIT,
        title="Limit",
        description="Limit number of User Summaries returned in the response.",
        gt=0,
    ),
    cursor: Optional[str] = Query(
        None,
        title="Page cursor",
        description=(
            "The cursor of the requested page, provided in the next_cursor key of the previous "
            "response. Leave empty to query for the first page."
        ),
    ),
) -> dto.UserSummaryPaginatedResponse:
    """
    List view for paginating and or filtering User Summaries.

    \f
    :return:
    """
    user_summary_filter = dto.UserSummaryFilter(limit=limit, cursor=cursor)
    user_summary_paginated_response = await domain.list_users(filter=user_summary_filter)

    return user_summary_paginated_response


# DEMO: show very verbose documentation around a required path parameter
@router.get("/users/{user_id}", response_model=dto.User)
async def get_user(
    user_id: dto.UserID = Path(..., title="User ID", description="The ID of the User to get.")
) -> dto.JSON:
    """
    Detail view for getting one User by ID.

    \f
    :return:
    """
    user = await domain.find_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user.dict()
