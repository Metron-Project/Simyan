import platform
from typing import Any

import pytest
from responses import RequestsMock as Mocker
from responses.matchers import query_param_matcher

from simyan import __version__
from simyan.comicvine import Comicvine
from simyan.resources import ORIGIN
from simyan.schemas.origin import BasicOrigin


def test_default_user_agent(session: Comicvine) -> None:
    expected_user_agent = f"Simyan/{__version__} ({platform.system()}: {platform.release()}; Python v{platform.python_version()})"  # noqa: E501
    assert session._session.headers["User-Agent"] == expected_user_agent


def test_custom_user_agent(api_key: str) -> None:
    custom_ua = "MyCustomApp/1.0"
    session = Comicvine(api_key=api_key, user_agent=custom_ua)
    assert session._session.headers["User-Agent"] == custom_ua


def test_empty_string_user_agent_uses_default(api_key: str) -> None:
    session = Comicvine(api_key=api_key, user_agent="")
    expected_user_agent = f"Simyan/{__version__} ({platform.system()}: {platform.release()}; Python v{platform.python_version()})"  # noqa: E501
    assert session._session.headers["User-Agent"] == expected_user_agent


def test_headers_structure(api_key: str) -> None:
    session = Comicvine(api_key=api_key)
    assert "Accept" in session._session.headers
    assert "User-Agent" in session._session.headers
    assert session._session.headers["Accept"] == "application/json"


@pytest.mark.parametrize(
    ("total_results", "max_results", "expected_requests"),
    [(3, None, 1), (100, None, 1), (250, None, 3), (250, 20, 1)],
    ids=["short-page", "page-boundary", "multi-page", "max-results"],
)
def test_offset_stops_at_end_of_result_set(
    mock_session: Comicvine,
    monkeypatch: pytest.MonkeyPatch,
    total_results: int,
    max_results: int | None,
    expected_requests: int,
) -> None:
    params = {"filter": "volume:1"}
    requests: list[dict[str, str]] = []

    def fake_request(
        method: str, endpoint: str, params: dict[str, str] | None = None
    ) -> dict[str, Any]:
        assert method == "GET"
        assert endpoint == "/issues/"
        request_params = dict(params or {})
        requests.append(request_params)
        offset = int(request_params["offset"])
        limit = int(request_params["limit"])
        page = [{"id": result} for result in range(offset, min(offset + limit, total_results))]
        return {"results": page, "number_of_total_results": total_results}

    monkeypatch.setattr(mock_session, "_request", fake_request)

    results = mock_session._offset("/issues/", params=params, max_results=max_results)

    assert len(results) == min(total_results, max_results or total_results)
    assert len(requests) == expected_requests


@pytest.mark.parametrize(
    ("total_results", "max_results", "expected_requests"),
    [(7, None, 1), (10, None, 1), (25, None, 3), (50, 20, 2)],
    ids=["short-page", "page-boundary", "multi-page", "max-results"],
)
def test_paginate_stops_at_end_of_result_set(
    mock_session: Comicvine,
    monkeypatch: pytest.MonkeyPatch,
    total_results: int,
    max_results: int | None,
    expected_requests: int,
) -> None:
    params = {"query": "x"}
    requests: list[dict[str, str]] = []

    def fake_request(
        method: str, endpoint: str, params: dict[str, str] | None = None
    ) -> dict[str, Any]:
        assert method == "GET"
        assert endpoint == "/search/"
        request_params = dict(params or {})
        requests.append(request_params)
        page_number = int(request_params["page"])
        offset = (page_number - 1) * 10
        page = [{"id": result} for result in range(offset, min(offset + 10, total_results))]
        return {"results": page, "number_of_total_results": total_results}

    monkeypatch.setattr(mock_session, "_request", fake_request)

    results = mock_session._paginate("/search/", params=params, max_results=max_results)

    assert len(results) == min(total_results, max_results or total_results)
    assert len(requests) == expected_requests


def test_pagination_does_not_mutate_params(
    mock_session: Comicvine, mock_params: dict[str, str]
) -> None:
    params = {"filter": "name:Mutant"}
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = f"https://comicvine.gamespot.mock/api{ORIGIN.plural_endpoint()}"
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params | params | {"offset": "0", "limit": "100"})],
            status=200,
            json={
                "results": [
                    BasicOrigin(
                        api_url="https://comicvine.gamespot.com",
                        id=1,
                        name="Test",
                        site_url="https://comicvine.gamespot.com",
                    ).model_dump(mode="json", by_alias=True)
                ],
                "number_of_total_results": 1,
                "status_code": 1,
            },
        )
        mock_session.list_origins(params)
    assert params == {"filter": "name:Mutant"}
