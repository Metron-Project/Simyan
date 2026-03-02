from datetime import datetime

import pytest

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


def test_get_location_fail(session: Comicvine) -> None:
    with pytest.raises(ServiceError):
        session.get_location(location_id=-1)


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


def test_search_location(session: Comicvine) -> None:
    results = session.search(resource=ComicvineResource.LOCATION, query="Earth")
    assert all(isinstance(x, BasicLocation) for x in results)
