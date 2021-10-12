"""
The Test Volume module.

This module contains tests for Volume objects.
"""
import pytest

from simyan.exceptions import APIError

FIRST_ISSUE_ID = 111265
ID = 18216
ISSUE_COUNT = 67
LAST_ISSUE_ID = 278617
NAME = "Green Lantern"
PUBLISHER_ID = 10
START_YEAR = 2005


def test_volume(comicvine):
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


def test_volume_fail(comicvine):
    """Test for a non-existent volume."""
    with pytest.raises(APIError):
        comicvine.volume(-1)


def test_volume_list(comicvine):
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


def test_volume_list_empty(comicvine):
    """Test VolumeList with no results."""
    results = comicvine.volume_list({"filter": "name:INVALID"})
    assert len(results) == 0
