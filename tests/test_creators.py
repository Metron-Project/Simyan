"""
Test Creators module.

This module contains tests for Creator objects.
"""
import datetime

import pytest

from Simyan.exceptions import APIError

COUNTRY = "United States"
DATE_OF_BIRTH = None
DATE_OF_DEATH = None
EMAIL = None
GENDER = 1
HOMETOWN = None
ID = 41853
ISSUE_COUNT = None
ISSUE_ID = 878411
ISSUE_NAME = None
NAME = "Peter J. Tomasi"
STORY_ARC_ID = 60628
STORY_ARC_NAME = "Destiny"
VOLUME_ID = 4958
VOLUME_NAME = "DC Universe: Trinity"
WEBSITE = None


def test_creator(comicvine):
    """Test for a known creator."""
    result = comicvine.creator(ID)
    assert result.country == COUNTRY
    assert result.date_of_birth == DATE_OF_BIRTH
    assert result.date_of_death == DATE_OF_DEATH
    assert result.email == EMAIL
    assert result.gender == GENDER
    assert result.hometown == HOMETOWN
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.issues[0].id == ISSUE_ID
    assert result.issues[0].name == ISSUE_NAME
    assert result.name == NAME
    assert result.story_arcs[0].id == STORY_ARC_ID
    assert result.story_arcs[0].name == STORY_ARC_NAME
    assert result.volumes[0].id == VOLUME_ID
    assert result.volumes[0].name == VOLUME_NAME
    assert result.website == WEBSITE


def test_creator_fail(comicvine):
    """Test for a non-existant creator."""
    with pytest.raises(APIError):
        comicvine.creator(-1)


def test_creator_with_dob(comicvine):
    """Test creators date of birth & death."""
    kirby = comicvine.creator(5614)
    assert kirby.date_of_birth == datetime.date(1917, 8, 28)
    assert kirby.date_of_death == datetime.date(1994, 2, 6)


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
