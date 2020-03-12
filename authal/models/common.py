from typing import Any, Dict

import motor.motor_asyncio
from bson import ObjectId

from authal import config, dto

_db = None
MONGO_DUPLICATION_ERROR = 11000

BSONDocument = Dict[str, Any]


async def get_db():
    global _db
    if _db is None:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            host=config.MONGODB_URL,
            tz_aware=True,
            maxPoolSize=config.MONGO_MAX_POOL_SIZE,
            retryWrites=False,
        )
        _db = client.get_database()

    return _db


def bson_to_user_id(obj_id: ObjectId) -> dto.UserID:
    return dto.UserID(str(obj_id))
