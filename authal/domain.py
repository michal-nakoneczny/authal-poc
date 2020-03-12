import logging
from typing import Optional

import authal.exceptions
import authal.libs.dates
from authal import dto
from authal.models import user_model
from authal.services import cat_api

logger = logging.getLogger(__name__)


async def create_user(new_user: dto.UnsavedUser) -> dto.User:
    now = authal.libs.dates.get_utcnow()
    user = await user_model.create_user(new_user, now)
    return user


async def list_users(
    filter: Optional[dto.UserSummaryFilter] = None
) -> dto.UserSummaryPaginatedResponse:

    filter = filter or dto.UserSummaryFilter()

    user_summaries = await user_model.list_users(filter)
    next_cursor = None
    if user_summaries and len(user_summaries) == filter.limit:
        next_cursor = user_summaries[-1].id

    return dto.UserSummaryPaginatedResponse(results=user_summaries, next_cursor=next_cursor)


async def find_user_by_id(user_id: dto.UserID) -> Optional[dto.User]:
    return await user_model.find_user_by_id(user_id=user_id)


async def get_version_from_cat_api():
    cat_api_version = await cat_api.get_version()
    return cat_api_version
