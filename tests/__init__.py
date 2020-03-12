from datetime import datetime, timedelta
from typing import Any, Dict, NamedTuple, Optional

import requests
from asynctest import mock

import authal.models.common


class MatchAnyOfType:
    """
    >>> MatchAnyOfType(str) == ''
    True
    >>> MatchAnyOfType(int) == 6
    True
    >>> MatchAnyOfType(int) == 6.5
    False
    >>> MatchAnyOfType(float) == 6.5
    True
    >>> MatchAnyOfType(int) == ''
    False
    >>> repr(MatchAnyOfType(int))
    'MatchAnyOfType(int)'
    >>> repr(MatchAnyOfType((int, str)))
    'MatchAnyOfType((int, str))'
    """

    def __init__(self, type_to_match):
        self._type = type_to_match

    def __eq__(self, other) -> bool:
        return isinstance(other, self._type)

    def __repr__(self):
        if isinstance(self._type, tuple):
            type_names = ", ".join(_type.__name__ for _type in self._type)
            type_name = f"({type_names})"
        else:
            type_name = self._type.__name__
        return f"MatchAnyOfType({type_name})"


class UTCNowMock:
    """
    Usage:

    @UTCNowMock.patch(datetime(2019, 1, 1, 12, 0, 1))
    def my_function(mock_get_utc_now):

    or

    with UTCNowMock.patch(datetime(2019, 1, 1, 12, 0, 1)) as mock_utc_now:
    """

    def __init__(self, start_date: datetime):
        self.start_date = start_date
        self.elapsed_seconds = 0

    def utcnow(self) -> datetime:
        """
        :return: `datetime` incremented by 1 second every time this is called
        """
        new_value = self.start_date + timedelta(seconds=self.elapsed_seconds)
        self.elapsed_seconds += 1
        return new_value

    @classmethod
    def patch(cls, start_date: datetime):
        return cls(start_date)._patch()

    def _patch(self):
        return mock.patch("authal.libs.dates.get_utcnow", side_effect=self.utcnow)


def reset_collections():
    db = authal.models.common.get_db()
    names = db.list_collection_names()
    for name in names:
        db[name].delete_many({})


class MockResponse(NamedTuple):
    status_code: int
    body: Optional[Dict[str, Any]]

    def json(self) -> Optional[Dict[str, Any]]:
        return self.body

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(self.status_code, response=self)
