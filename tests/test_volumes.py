"""
The Test Volume module.

This module contains tests for Volume objects.
"""
import pytest

from simyan.exceptions import APIError
from simyan.session import Session as Comicvine

FIRST_ISSUE_ID = 111265
ID = 18216
ISSUE_COUNT = 67
LAST_ISSUE_ID = 278617
NAME = "Green Lantern"
PUBLISHER_ID = 10
START_YEAR = 2005


def test_volume(comicvine: Comicvine):
    """Test for a known volume."""
    result = comicvine.volume(ID)
    assert result.characters[0].id == 11202
    assert result.concepts[0].id == 41148
    assert result.creators[0].id == 40439
    assert result.first_issue.id == FIRST_ISSUE_ID
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.issues[0].id == 106713
    assert result.last_issue.id == LAST_ISSUE_ID
    assert result.locations[0].id == 47879
    assert result.name == NAME
    assert result.objects[0].id == 11202
    assert result.publisher.id == PUBLISHER_ID
    assert result.start_year == START_YEAR


def test_volume_invalid_start_year(comicvine: Comicvine):
    """Test the VolumeList with an invalid start year."""
    result = comicvine.volume(106032)
    assert result.start_year is None


def test_volume_no_start_year(comicvine: Comicvine):
    """Test the Volume with no start year."""
    result = comicvine.volume(88330)
    assert result.start_year is None


def test_volume_no_publisher(comicvine: Comicvine):
    """Test the Volume with no Publisher."""
    result = comicvine.volume(89312)
    assert result.publisher is None


def test_volume_fail(comicvine: Comicvine):
    """Test for a non-existent volume."""
    with pytest.raises(APIError):
        comicvine.volume(-1)


def test_volume_list(comicvine: Comicvine):
    """Test the VolumeList."""
    search_results = comicvine.volume_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.first_issue.id == FIRST_ISSUE_ID
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.last_issue.id == LAST_ISSUE_ID
    assert result.name == NAME
    assert result.publisher.id == PUBLISHER_ID
    assert result.start_year == START_YEAR


def test_volume_list_invalid_start_year(comicvine: Comicvine):
    """Test the VolumeList with an invalid start year."""
    search_results = comicvine.volume_list({"filter": "name:Archie"})
    result = [x for x in search_results if x.id == 106032][0]
    assert result.start_year is None


def test_volume_list_no_start_year(comicvine: Comicvine):
    """Test the VolumeList with no start year."""
    search_results = comicvine.volume_list({"filter": "name:The Flash"})
    result = [x for x in search_results if x.id == 88330][0]
    assert result.start_year is None


def test_volume_list_no_publisher(comicvine: Comicvine):
    """Test the VolumeList with no publisher."""
    search_results = comicvine.volume_list({"filter": "name:Archie"})
    result = [x for x in search_results if x.id == 89312][0]
    assert result.publisher is None


def test_volume_list_empty(comicvine: Comicvine):
    """Test VolumeList with no results."""
    results = comicvine.volume_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_volume_no_first_issue(comicvine: Comicvine):
    """Test Volume with no first_issue."""
    result = comicvine.volume(_id=92409)
    assert result.first_issue is None


def test_volume_no_last_issue(comicvine: Comicvine):
    """Test Volume with no last_issue."""
    result = comicvine.volume(_id=92409)
    assert result.last_issue is None


def test_volume_list_no_first_issue(comicvine: Comicvine):
    """Test VolumeList with no first_issue."""
    search_results = comicvine.volume_list(params={"filter": "name:Justice League"})
    result = [x for x in search_results if x.id == 92409][0]
    assert result.first_issue is None


def test_volume_list_no_last_issue(comicvine: Comicvine):
    """Test VolumeList with no last_issue."""
    search_results = comicvine.volume_list(params={"filter": "name:Justice League"})
    result = [x for x in search_results if x.id == 92409][0]
    assert result.last_issue is None
