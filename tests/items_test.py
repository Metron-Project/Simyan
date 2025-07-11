"""The Items test module.

This module contains tests for Item and BasicItem objects.
"""

from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.item import BasicItem


def test_get_item(session: Comicvine) -> None:
    """Test the get_item function with a valid id."""
    result = session.get_item(item_id=41361)
    assert result is not None
    assert result.id == 41361

    assert len(result.issues) == 3335
    assert len(result.story_arcs) == 457
    assert len(result.volumes) == 1006


def test_get_item_fail(session: Comicvine) -> None:
    """Test the get_item function with an invalid id."""
    with pytest.raises(ServiceError):
        session.get_item(item_id=-1)


def test_list_items(session: Comicvine) -> None:
    """Test the list_items function with a valid search query."""
    search_results = session.list_items({"filter": "name:Green Power Ring"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 41361)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/object/4055-41361/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 50)
    assert result.first_issue.id == 123898
    assert result.issue_count == 3335
    assert result.name == "Green Power Ring"
    assert str(result.site_url) == "https://comicvine.gamespot.com/green-power-ring/4055-41361/"
    assert result.start_year == 1940


def test_list_items_empty(session: Comicvine) -> None:
    """Test the list_items function with an invalid search query."""
    results = session.list_items({"filter": "name:INVALID"})
    assert len(results) == 0


def test_list_items_max_results(session: Comicvine) -> None:
    """Test the list_items function with max results."""
    results = session.list_items(max_results=10)
    assert len(results) == 10


def test_search_item(session: Comicvine) -> None:
    """Test the search function for a list of Items."""
    results = session.search(resource=ComicvineResource.ITEM, query="Ring")
    assert all(isinstance(x, BasicItem) for x in results)
