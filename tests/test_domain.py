from datetime import datetime, timezone

import asynctest
import pytest
from asynctest import mock

from authal import domain, dto
from tests import fixtures

UTC = timezone.utc


@asynctest.patch("authal.libs.dates.get_utcnow")
@asynctest.patch("authal.models.user_model.create_user")
@pytest.mark.asyncio
async def test_user_create_success(mock_user_model_create_user: mock.Mock, mock_utcnow: mock.Mock):
    mock_utcnow.return_value = datetime(2019, 1, 1, 23, 59, tzinfo=UTC)
    mock_user_model_create_user.return_value = fixtures.user_fixture()

    result = await domain.create_user(fixtures.new_user_fixture())

    assert result == fixtures.user_fixture()
    mock_utcnow.assert_called_once()
    mock_user_model_create_user.assert_called_once_with(
        fixtures.new_user_fixture(), datetime(2019, 1, 1, 23, 59, tzinfo=UTC)
    )


@asynctest.mock.patch("authal.models.user_model.list_users")
@pytest.mark.asyncio
async def test_list_users(mock_user_model_list_users: mock.Mock):
    mock_user_model_list_users.return_value = [fixtures.user_summary_fixture()]

    result = await domain.list_users()

    assert result == dto.UserSummaryPaginatedResponse(
        results=[fixtures.user_summary_fixture()], next_cursor=None
    )


@asynctest.patch("authal.models.user_model.list_users")
@pytest.mark.asyncio
async def test_list_users_pagination(mock_user_model_list_users: mock.Mock):
    mock_user_model_list_users.return_value = [
        dto.UserSummary(
            id=dto.UserID("00000000000000000000000a"),
            email="client_a@gengo.com",
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
            id=dto.UserID("00000000000000000000000c"),
            email="client_c@gengo.com",
            ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
            mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
        ),
    ]

    result = await domain.list_users(dto.UserSummaryFilter(limit=3))

    assert result == dto.UserSummaryPaginatedResponse(
        results=[
            dto.UserSummary(
                id=dto.UserID("00000000000000000000000a"),
                email="client_a@gengo.com",
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
                id=dto.UserID("00000000000000000000000c"),
                email="client_c@gengo.com",
                ctime=datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
                mtime=datetime(2020, 1, 2, 0, 0, tzinfo=UTC),
            ),
        ],
        next_cursor=dto.UserID("00000000000000000000000c"),
    )


@asynctest.mock.patch("authal.models.user_model.find_user_by_id")
@pytest.mark.asyncio
async def test_find_user_details(mock_user_model_find_user_by_id: mock.Mock):
    mock_user_model_find_user_by_id.return_value = fixtures.user_fixture()
    result = await domain.find_user_by_id(user_id=dto.UserID("000000000000000000000001"))

    assert result == fixtures.user_fixture()
    mock_user_model_find_user_by_id.assert_called_once_with(
        user_id=dto.UserID("000000000000000000000001")
    )


@asynctest.mock.patch("authal.services.cat_api.get_version")
@pytest.mark.asyncio
async def test_get_version_from_cat_api(mock_services_cat_api_get_version: mock.Mock):
    mock_services_cat_api_get_version.return_value = {"version": "6.6.6"}
    result = await domain.get_version_from_cat_api()

    assert result == {"version": "6.6.6"}
    mock_services_cat_api_get_version.assert_called_once_with()
