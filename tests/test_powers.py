"""The Powers test module.

This module contains tests for Power and PowerEntry objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.power import PowerEntry


def test_power(session: Comicvine) -> None:
    """Test using the power endpoint with a valid power_id."""
    result = session.get_power(power_id=1)
    assert result is not None
    assert result.id == 1

    assert result.api_url == "https://comicvine.gamespot.com/api/power/4035-1/"
    assert len(result.characters) == 8040
    assert result.date_added.astimezone() == datetime(2008, 6, 6, 11, 28, 15).astimezone()
    assert result.name == "Flight"
    assert (
        result.site_url
        == "https://comicvine.gamespot.com/characters/?wikiSlug=flight&wikiTypeId=4035&wikiId=1&powers%5B%5D=1"
    )


def test_power_fail(session: Comicvine) -> None:
    """Test using the power endpoint with an invalid power_id."""
    with pytest.raises(ServiceError):
        session.get_power(power_id=-1)


def test_power_list(session: Comicvine) -> None:
    """Test using the list powers endpoint with a valid search query."""
    search_results = session.list_powers({"filter": "name:Flight"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 1)
    assert result is not None

    assert result.api_url == "https://comicvine.gamespot.com/api/power/4035-1/"
    assert result.date_added.astimezone() == datetime(2008, 6, 6, 11, 28, 15).astimezone()
    assert result.name == "Flight"
    assert (
        result.site_url
        == "https://comicvine.gamespot.com/characters/?wikiSlug=flight&wikiTypeId=4035&wikiId=1&powers%5B%5D=1"
    )


def test_power_list_empty(session: Comicvine) -> None:
    """Test using the list powers endpoint with an invalid search query."""
    results = session.list_powers({"filter": "name:INVALID"})
    assert len(results) == 0


def test_power_list_max_results(session: Comicvine) -> None:
    """Test list powers endpoint with max results."""
    results = session.list_powers(max_results=10)
    assert len(results) == 10


def test_search_power(session: Comicvine) -> None:
    """Test using the search endpoint for a list of Powers."""
    results = session.search(resource=ComicvineResource.POWER, query="Flight")
    assert all(isinstance(x, PowerEntry) for x in results)
