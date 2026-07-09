from datetime import datetime

import pytest
from responses import RequestsMock as Mocker
from responses.matchers import query_param_matcher

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.publisher import BasicPublisher


def test_get_publisher(session: Comicvine) -> None:
    result = session.get_publisher(publisher_id=364)
    assert result is not None
    assert result.id == 364

    assert len(result.characters) == 779
    assert len(result.story_arcs) == 37
    assert len(result.teams) == 43
    assert len(result.volumes) == 4769


def test_get_publisher_fail(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = f"https://comicvine.gamespot.mock/api/publisher/{ComicvineResource.PUBLISHER.resource_id}--1/"
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params)],
            status=404,
            json={"detail": "Not found."},
        )
        with pytest.raises(ServiceError):
            mock_session.get_publisher(publisher_id=-1)
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)


def test_list_publishers(session: Comicvine) -> None:
    search_results = session.list_publishers({"filter": "name:DC Comics"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 10)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/publisher/4010-10/"
    assert result.date_added == datetime(2008, 6, 6, 11, 8)
    assert result.location_address == "4000 Warner Blvd"
    assert result.location_city == "Burbank"
    assert result.location_state == "California"
    assert result.name == "DC Comics"
    assert str(result.site_url) == "https://comicvine.gamespot.com/dc-comics/4010-10/"


def test_list_publishers_empty(session: Comicvine) -> None:
    results = session.list_publishers({"filter": "name:Invalid Publisher Name"})
    assert len(results) == 0


def test_list_publishers_max_results(session: Comicvine) -> None:
    results = session.list_publishers(max_results=10)
    assert len(results) == 10


def test_search_deprecation(session: Comicvine) -> None:
    with pytest.deprecated_call():
        results = session.search(resource=ComicvineResource.PUBLISHER, query="DC")
        assert all(isinstance(x, BasicPublisher) for x in results)


def test_search_publisher(session: Comicvine) -> None:
    results = session.search_publishers(query="DC")
    assert all(isinstance(x, BasicPublisher) for x in results)
