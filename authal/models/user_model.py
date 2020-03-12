import logging
from datetime import datetime
from typing import List, Optional

import bson.errors
from bson import ObjectId

from authal import dto
from authal.models.common import BSONDocument, bson_to_user_id, get_db

_COLLECTION = "users"
_SUMMARY_FIELDS = ["_id", "email", "ctime", "mtime"]


logger = logging.getLogger(__name__)


async def _get_collection():
    db = await get_db()
    return db[_COLLECTION]


# DEMO: inserting one document with motor in an async function
async def create_user(new_user: dto.UnsavedUser, now: datetime) -> dto.User:
    collection = await _get_collection()
    result = await collection.insert_one(_to_bson(new_user, now))
    user_id = bson_to_user_id(result.inserted_id)
    return dto.User(id=user_id, email=new_user.email, ctime=now, mtime=now)


# DEMO: getting matching documents using motor in an async function
async def list_users(filter: dto.UserSummaryFilter) -> List[dto.UserSummary]:
    match = {}
    if filter.cursor is not None:
        try:
            match["_id"] = {"$lt": ObjectId(filter.cursor)}
        except bson.errors.InvalidId:
            return []

    sort = [("_id", -1)]
    collection = await _get_collection()
    results = collection.find(match, sort=sort, projection=_SUMMARY_FIELDS).limit(filter.limit)

    user_summaries = [_summary_from_bson(document) async for document in results]
    return user_summaries


# DEMO: getting one matching document using motor in an async function
async def find_user_by_id(user_id: dto.UserID) -> Optional[dto.User]:
    try:
        obj_id = ObjectId(user_id)
    except bson.errors.InvalidId:
        return None

    collection = await _get_collection()
    found = await collection.find_one({"_id": obj_id})

    if found is None:
        return None

    return _from_bson(found)


def _to_bson(new_user: dto.UnsavedUser, now: datetime) -> BSONDocument:
    return {"email": new_user.email, "ctime": now, "mtime": now}


def _from_bson(user: BSONDocument) -> dto.User:
    return dto.User(
        id=bson_to_user_id(user["_id"]),
        email=user["email"],
        ctime=user["ctime"],
        mtime=user["mtime"],
    )


def _summary_from_bson(user: BSONDocument) -> dto.UserSummary:
    return dto.UserSummary(
        id=bson_to_user_id(user["_id"]),
        email=user["email"],
        ctime=user["ctime"],
        mtime=user["mtime"],
    )
