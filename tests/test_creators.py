"""
The Test Creators module.

This module contains tests for Creator objects.
"""
from datetime import date

import pytest

from simyan.exceptions import APIError

COUNTRY = "United States"
DATE_OF_BIRTH = date(year=1973, month=1, day=25)
DATE_OF_DEATH = None
EMAIL = None
GENDER = 1
HOMETOWN = "Detroit, MI"
ID = 40439
ISSUE_COUNT = None
NAME = "Geoff Johns"
WEBSITE = "http://www.geoffjohns.com"


def test_creator(comicvine):
    """Test for a known creator."""
    result = comicvine.creator(ID)
    assert result.country == COUNTRY
    assert result.characters[0].id == 148828
    assert result.date_of_birth == DATE_OF_BIRTH
    assert result.date_of_death == DATE_OF_DEATH
    assert result.email == EMAIL
    assert result.gender == GENDER
    assert result.hometown == HOMETOWN
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.issues[0].id == 882780
    assert result.name == NAME
    assert len(result.story_arcs) == 0
    assert result.volumes[0].id == 5261
    assert result.website == WEBSITE


def test_creator_fail(comicvine):
    """Test for a non-existent creator."""
    with pytest.raises(APIError):
        comicvine.creator(-1)


def test_creator_with_dob(comicvine):
    """Test creators date of birth & death."""
    kirby = comicvine.creator(5614)
    assert kirby.date_of_birth == date(1917, 8, 28)
    assert kirby.date_of_death == date(1994, 2, 6)


def test_creator_list(comicvine):
    """Test the CreatorsList."""
    search_results = comicvine.creator_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.country == COUNTRY
    assert result.date_of_birth == DATE_OF_BIRTH
    assert result.date_of_death == DATE_OF_DEATH
    assert result.email == EMAIL
    assert result.gender == GENDER
    assert result.hometown == HOMETOWN
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.name == NAME
    assert result.website == WEBSITE


def test_creator_list_empty(comicvine):
    """Test CreatorList with bad response."""
    results = comicvine.creator_list({"filter": "name:INVALID"})
    assert len(results) == 0
