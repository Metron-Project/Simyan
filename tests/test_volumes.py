"""The Volumes test module.

This module contains tests for Volume and VolumeEntry objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.volume import VolumeEntry


def test_volume(session: Comicvine) -> None:
    """Test using the volume endpoint with a valid volume_id."""
    result = session.get_volume(volume_id=18216)
    assert result is not None
    assert result.id == 18216

    assert result.api_url == "https://comicvine.gamespot.com/api/volume/4050-18216/"
    assert len(result.characters) == 367
    assert len(result.concepts) == 18
    assert len(result.creators) == 95
    assert result.date_added.astimezone() == datetime(2008, 6, 6, 11, 8, 33).astimezone()
    assert result.first_issue.id == 111265
    assert result.issue_count == 67
    assert len(result.issues) == 67
    assert result.last_issue.id == 278617
    assert len(result.locations) == 48
    assert result.name == "Green Lantern"
    assert len(result.objects) == 367
    assert result.publisher.id == 10
    assert result.site_url == "https://comicvine.gamespot.com/green-lantern/4050-18216/"
    assert result.start_year == 2005


def test_volume_fail(session: Comicvine) -> None:
    """Test using the volume endpoint with an invalid volume_id."""
    with pytest.raises(ServiceError):
        session.get_volume(volume_id=-1)


def test_volume_list(session: Comicvine) -> None:
    """Test using the volume_list endpoint with a valid search."""
    search_results = session.list_volumes({"filter": "name:Green Lantern"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 18216)
    assert result is not None

    assert result.api_url == "https://comicvine.gamespot.com/api/volume/4050-18216/"
    assert result.date_added.astimezone() == datetime(2008, 6, 6, 11, 8, 33).astimezone()
    assert result.first_issue.id == 111265
    assert result.issue_count == 67
    assert result.last_issue.id == 278617
    assert result.name == "Green Lantern"
    assert result.publisher.id == 10
    assert result.site_url == "https://comicvine.gamespot.com/green-lantern/4050-18216/"
    assert result.start_year == 2005


def test_volume_list_empty(session: Comicvine) -> None:
    """Test using the volume_list endpoint with an invalid search."""
    results = session.list_volumes({"filter": "name:INVALID"})
    assert len(results) == 0


def test_volume_list_max_results(session: Comicvine) -> None:
    """Test volume_list endpoint with max_results."""
    results = session.list_volumes({"filter": "name:Green Lantern"}, max_results=10)
    assert len(results) == 10


def test_search_volume(session: Comicvine) -> None:
    """Test using the search endpoint for a list of Volumes."""
    results = session.search(resource=ComicvineResource.VOLUME, query="Lantern")
    assert all(isinstance(x, VolumeEntry) for x in results)


def test_search_volume_max_results(session: Comicvine) -> None:
    """Test search endpoint with max_results."""
    results = session.search(resource=ComicvineResource.VOLUME, query="Lantern", max_results=10)
    assert all(isinstance(x, VolumeEntry) for x in results)
    assert len(results) == 10


def test_volume_invalid_start_year(session: Comicvine) -> None:
    """Test volume endpoint to return result with an invalid start year."""
    result = session.get_volume(volume_id=106032)
    assert result.start_year is None


def test_volume_list_invalid_start_year(session: Comicvine) -> None:
    """Test volume_list endpoint to return result with an invalid start year."""
    search_results = session.list_volumes({"filter": "name:Archie"})
    result = next(x for x in search_results if x.id == 106032)
    assert result.start_year is None


def test_volume_no_start_year(session: Comicvine) -> None:
    """Test volume endpoint to return result with no start year."""
    result = session.get_volume(volume_id=88330)
    assert result.start_year is None


def test_volume_list_no_start_year(session: Comicvine) -> None:
    """Test volume_list endpoint to return result with no start year."""
    search_results = session.list_volumes({"filter": "name:The Flash"})
    result = next(x for x in search_results if x.id == 88330)
    assert result.start_year is None
