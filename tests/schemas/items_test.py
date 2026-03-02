from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.item import BasicItem


def test_get_item(session: Comicvine) -> None:
    result = session.get_item(item_id=41361)
    assert result is not None
    assert result.id == 41361

    assert len(result.issues) == 3393
    assert len(result.story_arcs) == 456
    assert len(result.volumes) == 1033


def test_get_item_fail(session: Comicvine) -> None:
    with pytest.raises(ServiceError):
        session.get_item(item_id=-1)


def test_list_items(session: Comicvine) -> None:
    search_results = session.list_items({"filter": "name:Green Power Ring"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 41361)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/object/4055-41361/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 50)
    assert result.first_issue.id == 144069
    assert result.issue_count == 3393
    assert result.name == "Green Power Ring"
    assert str(result.site_url) == "https://comicvine.gamespot.com/green-power-ring/4055-41361/"
    assert result.start_year == 1940


def test_list_items_empty(session: Comicvine) -> None:
    results = session.list_items({"filter": "name:Invalid Item Name"})
    assert len(results) == 0


def test_list_items_max_results(session: Comicvine) -> None:
    results = session.list_items(max_results=10)
    assert len(results) == 10


def test_search_item(session: Comicvine) -> None:
    results = session.search(resource=ComicvineResource.ITEM, query="Ring")
    assert all(isinstance(x, BasicItem) for x in results)
