from datetime import datetime

import pytest
from responses import RequestsMock as Mocker
from responses.matchers import query_param_matcher

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.volume import BasicVolume


def test_get_volume(session: Comicvine) -> None:
    result = session.get_volume(volume_id=18216)
    assert result is not None
    assert result.id == 18216

    assert len(result.characters) == 368
    assert len(result.concepts) == 3
    assert len(result.creators) == 95
    assert len(result.issues) == 67
    assert len(result.locations) == 46
    assert len(result.objects) == 368


def test_get_volume_fail(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = (
            f"https://comicvine.gamespot.mock/api/volume/{ComicvineResource.VOLUME.resource_id}--1/"
        )
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params)],
            status=404,
            json={"detail": "Not found."},
        )
        with pytest.raises(ServiceError):
            mock_session.get_volume(volume_id=-1)
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)


def test_list_volumes(session: Comicvine) -> None:
    search_results = session.list_volumes({"filter": "name:Green Lantern"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 18216)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/volume/4050-18216/"
    assert result.date_added == datetime(2008, 6, 6, 11, 8, 33)
    assert result.first_issue.id == 111265
    assert result.issue_count == 67
    assert result.last_issue.id == 278617
    assert result.name == "Green Lantern"
    assert result.publisher.id == 10
    assert str(result.site_url) == "https://comicvine.gamespot.com/green-lantern/4050-18216/"
    assert result.start_year == 2005


def test_list_volumes_empty(session: Comicvine) -> None:
    results = session.list_volumes({"filter": "name:Invalid Volume Name"})
    assert len(results) == 0


def test_list_volumes_max_results(session: Comicvine) -> None:
    results = session.list_volumes(max_results=10)
    assert len(results) == 10


def test_search_deprecation(session: Comicvine) -> None:
    with pytest.deprecated_call():
        results = session.search(resource=ComicvineResource.VOLUME, query="Lantern")
        assert all(isinstance(x, BasicVolume) for x in results)


def test_search_volume(session: Comicvine) -> None:
    results = session.search_volumes(query="Lantern")
    assert all(isinstance(x, BasicVolume) for x in results)
