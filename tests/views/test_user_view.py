from datetime import datetime, timezone

import asynctest
import pytest
from asynctest import mock
from starlette.testclient import TestClient

from authal import dto
from authal.main import app
from tests import fixtures

UTC = timezone.utc
client = TestClient(app)


@asynctest.mock.patch("authal.domain.create_user")
def test_user_create_success(mock_domain_create_user: mock.Mock):
    body = fixtures.unsaved_user_json_fixture()
    mock_domain_create_user.return_value = fixtures.user_fixture()

    response = client.post("/users", json=body)

    expected_response = (201, fixtures.user_json_fixture())
    assert (response.status_code, response.json()) == expected_response
    mock_domain_create_user.assert_called_once_with(fixtures.unsaved_user_fixture())


# DEMO: talk about dwefault error detail responses
@asynctest.mock.patch("authal.domain.create_user")
def test_user_create_bad_request(mock_create: mock.Mock):
    response = client.post("/users", json={})

    expected_response = (
        400,
        {
            "detail": [
                {
                    "loc": ["body", "unsaved_user", "email"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
            "demo_errors": [{"body.unsaved_user.email": ["field required"]}],
        },
    )
    assert (response.status_code, response.json()) == expected_response
    assert mock_create.call_count == 0


@asynctest.mock.patch("authal.domain.list_users")
def test_list_users(mock_domain_list_users: mock.Mock):
    mock_domain_list_users.return_value = dto.UserSummaryPaginatedResponse(
        results=[fixtures.user_summary_fixture()], next_cursor=None
    )

    response = client.get("/users")

    expected_response = (
        200,
        {"results": [fixtures.user_summary_json_fixture()], "next_cursor": None},
    )
    assert (response.status_code, response.json()) == expected_response
    assert mock_domain_list_users.called_once_with()


@asynctest.mock.patch("authal.domain.list_users")
def test_list_users_pagination(mock_domain_list_users: mock.Mock):
    mock_domain_list_users.return_value = dto.UserSummaryPaginatedResponse(
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

    response = client.get("/users?limit=3")

    expected_response = (
        200,
        {
            "results": [
                {
                    "id": "00000000000000000000000a",
                    "email": "client_a@gengo.com",
                    "ctime": "2020-01-01T00:00:00+00:00",
                    "mtime": "2020-01-02T00:00:00+00:00",
                },
                {
                    "id": "00000000000000000000000b",
                    "email": "client_b@gengo.com",
                    "ctime": "2020-01-01T00:00:00+00:00",
                    "mtime": "2020-01-02T00:00:00+00:00",
                },
                {
                    "id": "00000000000000000000000c",
                    "email": "client_c@gengo.com",
                    "ctime": "2020-01-01T00:00:00+00:00",
                    "mtime": "2020-01-02T00:00:00+00:00",
                },
            ],
            "next_cursor": "00000000000000000000000c",
        },
    )
    assert (response.status_code, response.json()) == expected_response
    assert mock_domain_list_users.called_once_with()


@pytest.mark.parametrize(
    "query_param_string, expected_error",
    [
        (
            "limit=x",
            {
                "detail": [
                    {
                        "loc": ["query", "limit"],
                        "msg": "value is not a valid integer",
                        "type": "type_error.integer",
                    }
                ],
                "demo_errors": [{"query.limit": ["value is not a valid integer"]}],
            },
        ),
        (
            "limit=-1",
            {
                "detail": [
                    {
                        "loc": ["query", "limit"],
                        "msg": "ensure this value is greater than 0",
                        "type": "value_error.number.not_gt",
                        "ctx": {"limit_value": 0},
                    }
                ],
                "demo_errors": [{"query.limit": ["ensure this value is greater than 0"]}],
            },
        ),
    ],
)
@asynctest.mock.patch("authal.domain.list_users")
def test_list_users_pagination_invalid_query_param(
    mock_domain_list_users: mock.Mock, query_param_string, expected_error
):
    response = client.get(f"/users?{query_param_string}")

    expected_response = (400, expected_error)
    assert (response.status_code, response.json()) == expected_response
    assert mock_domain_list_users.called_once_with()


@asynctest.mock.patch("authal.domain.find_user_by_id")
def test_user_detail_success(mock_domain_find_user_by_id: mock.Mock):
    mock_domain_find_user_by_id.return_value = fixtures.user_fixture()

    response = client.get("/users/00000000000000000000000a")

    expected_response = (200, fixtures.user_json_fixture())
    assert (response.status_code, response.json()) == expected_response
    mock_domain_find_user_by_id.assert_called_once_with(
        user_id=dto.UserID("00000000000000000000000a")
    )


@asynctest.mock.patch("authal.domain.find_user_by_id")
def test_user_detail_not_found(mock_domain_find_user_by_id: mock.Mock):
    mock_domain_find_user_by_id.return_value = None

    response = client.get("/users/00000000000000000000000f")

    expected_response = (404, {"detail": "User not found."})
    assert (response.status_code, response.json()) == expected_response
    mock_domain_find_user_by_id.assert_called_once_with(
        user_id=dto.UserID("00000000000000000000000f")
    )
