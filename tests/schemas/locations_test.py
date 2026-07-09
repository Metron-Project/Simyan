from datetime import datetime

import pytest
from responses import RequestsMock as Mocker
from responses.matchers import query_param_matcher

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.location import BasicLocation


def test_get_location(session: Comicvine) -> None:
    result = session.get_location(location_id=56000)
    assert result is not None
    assert result.id == 56000

    assert len(result.issues) == 28
    assert len(result.story_arcs) == 0
    assert len(result.volumes) == 1


def test_get_location_fail(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = f"https://comicvine.gamespot.mock/api/location/{ComicvineResource.LOCATION.resource_id}--1/"
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params)],
            status=404,
            json={"detail": "Not found."},
        )
        with pytest.raises(ServiceError):
            mock_session.get_location(location_id=-1)
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)


def test_list_locations(session: Comicvine) -> None:
    search_results = session.list_locations({"filter": "name:Odym"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 56000)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/location/4020-56000/"
    assert result.issue_count == 28
    assert result.date_added == datetime(2009, 1, 2, 16, 16, 18)
    assert result.first_issue.id == 149271
    assert result.name == "Odym"
    assert str(result.site_url) == "https://comicvine.gamespot.com/odym/4020-56000/"


def test_list_locations_empty(session: Comicvine) -> None:
    results = session.list_locations({"filter": "name:Invalid Location Name"})
    assert len(results) == 0


def test_list_locations_max_results(session: Comicvine) -> None:
    results = session.list_locations(max_results=10)
    assert len(results) == 10


def test_search_deprecation(session: Comicvine) -> None:
    with pytest.deprecated_call():
        results = session.search(resource=ComicvineResource.LOCATION, query="Earth")
        assert all(isinstance(x, BasicLocation) for x in results)


def test_search_location(session: Comicvine) -> None:
    results = session.search_locations(query="Earth")
    assert all(isinstance(x, BasicLocation) for x in results)
