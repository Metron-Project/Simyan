"""
The Test Creators module.

This module contains tests for Creator objects.
"""
from datetime import date

import pytest

from simyan.comicvine import Comicvine
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


def test_creator(session: Comicvine):
    """Test for a known creator."""
    result = session.creator(creator_id=ID)
    assert result.country == COUNTRY
    assert result.characters[0].id_ == 148828
    assert result.date_of_birth == DATE_OF_BIRTH
    assert result.date_of_death == DATE_OF_DEATH
    assert result.email == EMAIL
    assert result.gender == GENDER
    assert result.hometown == HOMETOWN
    assert result.id_ == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.issues[0].id_ == 916161
    assert result.name == NAME
    assert len(result.story_arcs) == 0
    assert result.volumes[0].id_ == 5261
    assert result.website == WEBSITE


def test_creator_fail(session: Comicvine):
    """Test for a non-existent creator."""
    with pytest.raises(APIError):
        session.creator(creator_id=-1)


def test_creator_with_dob(session: Comicvine):
    """Test creators date of birth & death."""
    kirby = session.creator(5614)
    assert kirby.date_of_birth == date(1917, 8, 28)
    assert kirby.date_of_death == date(1994, 2, 6)


def test_creator_list(session: Comicvine):
    """Test the CreatorsList."""
    search_results = session.creator_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id_ == ID][0]
    assert result.country == COUNTRY
    assert result.date_of_birth == DATE_OF_BIRTH
    assert result.date_of_death == DATE_OF_DEATH
    assert result.email == EMAIL
    assert result.gender == GENDER
    assert result.hometown == HOMETOWN
    assert result.id_ == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.name == NAME
    assert result.website == WEBSITE


def test_creator_list_empty(session: Comicvine):
    """Test CreatorList with bad response."""
    results = session.creator_list({"filter": "name:INVALID"})
    assert len(results) == 0
