"""
The Test Publishers module.

This module contains tests for Publisher objects.
"""
import pytest

from simyan.exceptions import APIError
from simyan.session import Session as Comicvine

ID = 10
LOCATION_ADDRESS = "4000 Warner Blvd"
LOCATION_CITY = "Burbank"
LOCATION_STATE = "California"
NAME = "DC Comics"


def test_publisher(comicvine: Comicvine):
    """Test for a known publisher."""
    result = comicvine.publisher(ID)
    assert result.characters[0].id == 1253
    assert result.id == ID
    assert result.location_address == LOCATION_ADDRESS
    assert result.location_city == LOCATION_CITY
    assert result.location_state == LOCATION_STATE
    assert result.name == NAME
    assert result.story_arcs[0].id == 40503
    assert result.teams[0].id == 5701
    assert result.volumes[0].id == 771


def test_publisher_fail(comicvine: Comicvine):
    """Test for a non-existent publisher."""
    with pytest.raises(APIError):
        comicvine.publisher(-1)


def test_publisher_list(comicvine: Comicvine):
    """Test the PublishersList."""
    search_results = comicvine.publisher_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.id == ID
    assert result.location_address == LOCATION_ADDRESS
    assert result.location_city == LOCATION_CITY
    assert result.location_state == LOCATION_STATE
    assert result.name == NAME


def test_publisher_list_empty(comicvine: Comicvine):
    """Test PublishersList with no results."""
    results = comicvine.publisher_list({"filter": "name:INVALID"})
    assert len(results) == 0
