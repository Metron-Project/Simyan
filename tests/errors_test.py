import pytest

from simyan.comicvine import Comicvine
from simyan.errors import AuthenticationError, ServiceError


def test_unauthorized() -> None:
    session = Comicvine(api_key="Invalid", cache=None)
    with pytest.raises(AuthenticationError):
        session.get_publisher(publisher_id=1)


def test_not_found(session: Comicvine) -> None:
    with pytest.raises(ServiceError):
        session._perform_get_request(endpoint="/invalid")  # noqa: SLF001


def test_timeout(comicvine_api_key: str) -> None:
    session = Comicvine(api_key=comicvine_api_key, timeout=1, cache=None)
    with pytest.raises(ServiceError):
        session.get_publisher(publisher_id=1)
