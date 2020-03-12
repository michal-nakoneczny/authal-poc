import logging
from datetime import datetime, timezone
from typing import List

import pytest
from bson import ObjectId

from authal import dto
from authal.models import user_model
from tests import fixtures

UTC = timezone.utc
logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
async def remove_users():
    logger.warning("removing all users")
    collection = await user_model._get_collection()
    await collection.delete_many({})


# DEMO: talk about async test cases
@pytest.mark.asyncio
async def test_create_user_success():
    collection = await user_model._get_collection()
    created = await user_model.create_user(
        new_user=fixtures.new_user_fixture(), now=datetime(2020, 1, 1, 0, 0, tzinfo=UTC)
    )
    assert created == dto.User(
        id=created.id,
        email="client@gengo.com",
        ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
        mtime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
    )
    actual = [document async for document in collection.find()]

    expected = [
        {
            "_id": ObjectId(created.id),
            "email": "client@gengo.com",
            "ctime": datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
            "mtime": datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
        }
    ]
    assert actual == expected


@pytest.mark.asyncio
async def test_list_user():
    collection = await user_model._get_collection()
    await collection.insert_one(fixtures.user_bson_fixture())

    actual = await user_model.list_users(dto.UserSummaryFilter(limit=20))

    expected = [fixtures.user_summary_fixture()]
    assert list(actual) == expected


@pytest.mark.parametrize(
    "user_summary_filter_kwargs, expected",
    [
        (
            {"limit": 3},
            [
                dto.UserSummary(
                    id=dto.UserID("00000000000000000000000f"),
                    email="client_f@gengo.com",
                    ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                    mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
                ),
                dto.UserSummary(
                    id=dto.UserID("00000000000000000000000e"),
                    email="client_e@gengo.com",
                    ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                    mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
                ),
                dto.UserSummary(
                    id=dto.UserID("00000000000000000000000d"),
                    email="client_d@gengo.com",
                    ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                    mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
                ),
            ],
        ),
        (
            {"limit": 3, "cursor": "00000000000000000000000d"},
            [
                dto.UserSummary(
                    id=dto.UserID("00000000000000000000000c"),
                    email="client_c@gengo.com",
                    ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                    mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
                ),
                dto.UserSummary(
                    id=dto.UserID("00000000000000000000000b"),
                    email="client_b@gengo.com",
                    ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                    mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
                ),
                dto.UserSummary(
                    id=dto.UserID("00000000000000000000000a"),
                    email="client_a@gengo.com",
                    ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                    mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
                ),
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_list_users_pagination(user_summary_filter_kwargs, expected):
    collection = await user_model._get_collection()
    await collection.insert_many(
        [
            {
                "_id": ObjectId("00000000000000000000000a"),
                "email": "client_a@gengo.com",
                "ctime": datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                "mtime": datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
            },
            {
                "_id": ObjectId("00000000000000000000000b"),
                "email": "client_b@gengo.com",
                "ctime": datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                "mtime": datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
            },
            {
                "_id": ObjectId("00000000000000000000000c"),
                "email": "client_c@gengo.com",
                "ctime": datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                "mtime": datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
            },
            {
                "_id": ObjectId("00000000000000000000000d"),
                "email": "client_d@gengo.com",
                "ctime": datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                "mtime": datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
            },
            {
                "_id": ObjectId("00000000000000000000000e"),
                "email": "client_e@gengo.com",
                "ctime": datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                "mtime": datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
            },
            {
                "_id": ObjectId("00000000000000000000000f"),
                "email": "client_f@gengo.com",
                "ctime": datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                "mtime": datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
            },
        ]
    )

    actual = await user_model.list_users(dto.UserSummaryFilter(**user_summary_filter_kwargs))

    assert list(actual) == expected


@pytest.mark.asyncio
async def test_list_user_filter_cursor_invalid_user_id():
    collection = await user_model._get_collection()
    await collection.insert_one(fixtures.user_bson_fixture())

    actual = await user_model.list_users(dto.UserSummaryFilter(limit=20, cursor=dto.UserID("1")))

    expected: List[dto.UserSummary] = []
    assert list(actual) == expected


@pytest.mark.asyncio
async def test_find_user_by_id_found():
    collection = await user_model._get_collection()
    await collection.insert_one(fixtures.user_bson_fixture())

    actual = await user_model.find_user_by_id(dto.UserID("00000000000000000000000a"))
    assert actual == fixtures.user_fixture()


@pytest.mark.asyncio
async def test_find_user_by_id_not_found():
    collection = await user_model._get_collection()
    await collection.insert_one(fixtures.user_bson_fixture())

    actual = await user_model.find_user_by_id(dto.UserID("00000000000000000000000f"))
    assert actual is None


@pytest.mark.asyncio
async def test_find_user_by_id_not_object_id():
    collection = await user_model._get_collection()
    await collection.insert_one(fixtures.user_bson_fixture())

    actual = await user_model.find_user_by_id(dto.UserID("abc"))
    assert actual is None


def test_from_bson():
    actual = user_model._from_bson(fixtures.user_bson_fixture())

    assert actual == fixtures.user_fixture()


def test_to_bson():
    actual = user_model._to_bson(
        fixtures.new_user_fixture(), datetime(2020, 1, 2, 0, 0, tzinfo=UTC)
    )

    assert actual == {
        "email": "client@gengo.com",
        "ctime": datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
        "mtime": datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
    }
