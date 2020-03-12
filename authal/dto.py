from datetime import datetime
from typing import Any, Dict, List, NewType, Optional

from pydantic import BaseModel

from authal import config

UserID = NewType("UserID", str)

JSON = Dict[str, Any]


# DEMO: show using Pydantic's models as DTOs
class UnsavedUser(BaseModel):
    email: str


class User(BaseModel):
    id: UserID
    email: str
    ctime: datetime
    mtime: datetime


class UserSummary(BaseModel):
    id: UserID
    email: str
    ctime: datetime
    mtime: datetime


class UserSummaryFilter(BaseModel):
    limit: Optional[int] = config.DEFAULT_PAGE_LIMIT
    cursor: Optional[str] = None


class UserSummaryPaginatedResponse(BaseModel):
    results: List[UserSummary]
    next_cursor: Optional[UserID]


class LinkResponse(BaseModel):
    href: str
    rel: str
    type: str


class StatusViewResponse(BaseModel):
    service: str
    version: str
    links: Optional[List[LinkResponse]]
