from datetime import datetime, timezone

from bson import ObjectId

from authal import dto

UTC = timezone.utc


def new_user_fixture() -> dto.UnsavedUser:
    return dto.UnsavedUser(email="client@gengo.com")


def user_fixture() -> dto.User:
    return dto.User(
        id=dto.UserID("00000000000000000000000a"),
        email="client@gengo.com",
        ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
        mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
    )


def user_bson_fixture() -> dto.JSON:
    return {
        "_id": ObjectId("00000000000000000000000a"),
        "email": "client@gengo.com",
        "ctime": datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
        "mtime": datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
    }


def user_json_fixture() -> dto.JSON:
    return {
        "id": "00000000000000000000000a",
        "email": "client@gengo.com",
        "ctime": "2020-01-01T00:00:00+00:00",
        "mtime": "2020-01-02T00:00:00+00:00",
    }


def user_summary_fixture() -> dto.UserSummary:
    return dto.UserSummary(
        id=dto.UserID("00000000000000000000000a"),
        email="client@gengo.com",
        ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
        mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
    )


def user_summary_json_fixture() -> dto.JSON:
    return {
        "id": "00000000000000000000000a",
        "email": "client@gengo.com",
        "ctime": "2020-01-01T00:00:00+00:00",
        "mtime": "2020-01-02T00:00:00+00:00",
    }


def unsaved_user_fixture() -> dto.UnsavedUser:
    return dto.UnsavedUser(email="client@gengo.com")


def unsaved_user_json_fixture() -> dto.JSON:
    return {"email": "client@gengo.com"}
