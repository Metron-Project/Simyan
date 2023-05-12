"""
The Items test module.

This module contains tests for Item and ItemEntry objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.item import ItemEntry


def test_item(session: Comicvine) -> None:
    """Test using the item endpoint with a valid item_id."""
    result = session.get_item(item_id=41361)
    assert result is not None
    assert result.item_id == 41361

    assert result.alias_list == ["Grüner Kraftring"]
    assert result.api_url == "https://comicvine.gamespot.com/api/object/4055-41361/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 50)
    assert result.first_issue.id_ == 123898
    assert result.issue_count == 3153
    assert len(result.issues) == 3153
    assert result.name == "Green Power Ring"
    assert result.site_url == "https://comicvine.gamespot.com/green-power-ring/4055-41361/"
    assert result.start_year == 1940
    assert len(result.story_arcs) == 561
    assert len(result.volumes) == 937


def test_item_fail(session: Comicvine) -> None:
    """Test using the item endpoint with an invalid item_id."""
    with pytest.raises(ServiceError):
        session.get_item(item_id=-1)


def test_item_list(session: Comicvine) -> None:
    """Test using the list items endpoint with a valid search query."""
    search_results = session.list_items({"filter": "name:Green Power Ring"})
    assert len(search_results) != 0
    result = [x for x in search_results if x.item_id == 41361][0]
    assert result is not None

    assert result.alias_list == ["Grüner Kraftring"]
    assert result.api_url == "https://comicvine.gamespot.com/api/object/4055-41361/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 50)
    assert result.first_issue.id_ == 123898
    assert result.issue_count == 3153
    assert result.name == "Green Power Ring"
    assert result.site_url == "https://comicvine.gamespot.com/green-power-ring/4055-41361/"
    assert result.start_year == 1940


def test_item_list_empty(session: Comicvine) -> None:
    """Test using the list items endpoint with an invalid search query."""
    results = session.list_items({"filter": "name:INVALID"})
    assert len(results) == 0


def test_item_list_max_results(session: Comicvine) -> None:
    """Test list items endpoint with max results."""
    results = session.list_items(max_results=10)
    assert len(results) == 10


def test_search_item(session: Comicvine) -> None:
    """Test using the search endpoint for a list of Items."""
    results = session.search(resource=ComicvineResource.ITEM, query="Ring")
    assert all(isinstance(x, ItemEntry) for x in results)
