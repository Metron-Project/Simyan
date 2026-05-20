import pytest
from requests.exceptions import Timeout
from responses import RequestsMock as Mocker
from responses.matchers import query_param_matcher

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import AuthenticationError, RateLimitError, ServiceError


def test_not_found(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = "https://comicvine.gamespot.mock/api/invalid/"
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params)],
            status=404,
            json={"detail": "Not found."},
        )
        with pytest.raises(ServiceError):
            mock_session._get_request(endpoint="/invalid")  # noqa: SLF001
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)


def test_timeout(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = f"https://comicvine.gamespot.mock/api/publisher/{ComicvineResource.PUBLISHER.resource_id}-1/"
        mock.get(url=url, match=[query_param_matcher(mock_params)], body=Timeout())
        with pytest.raises(ServiceError):
            mock_session.get_publisher(publisher_id=1)
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)


def test_authentication(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = f"https://comicvine.gamespot.mock/api/publisher/{ComicvineResource.PUBLISHER.resource_id}-1/"
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params)],
            status=401,
            json={"detail": "Invalid token."},
        )
        with pytest.raises(AuthenticationError):
            mock_session.get_publisher(publisher_id=1)
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)


def test_ratelimit(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = f"https://comicvine.gamespot.mock/api/publisher/{ComicvineResource.PUBLISHER.resource_id}-1/"
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params)],
            status=429,
            json={},
            headers={"Retry-After": "60"},
        )
        with pytest.raises(RateLimitError):
            mock_session.get_publisher(publisher_id=1)
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)
