"""
The Test Issues module.

This module contains tests for Issue objects.
"""
from datetime import date

import pytest

from simyan.exceptions import APIError

COVER_DATE = date(year=2005, month=7, day=1)
ID = 111265
NAME = "Airborne"
NUMBER = "1"
STORE_DATE = date(year=2005, month=5, day=18)
VOLUME_ID = 18216


def test_issue(comicvine):
    """Test for a known issue."""
    result = comicvine.issue(ID)
    assert result.characters[0].id == 22634
    assert result.concepts[0].id == 41148
    assert result.cover_date == COVER_DATE
    assert result.creators[0].id == 10945
    assert len(result.deaths) == 0
    assert result.first_appearance_characters is None
    assert result.first_appearance_concepts is None
    assert result.first_appearance_locations is None
    assert result.first_appearance_objects is None
    assert result.first_appearance_story_arcs is None
    assert result.first_appearance_teams is None
    assert result.id == ID
    assert result.locations[0].id == 56427
    assert result.name == NAME
    assert result.number == NUMBER
    assert result.objects[0].id == 41361
    assert result.store_date == STORE_DATE
    assert result.story_arcs[0].id == 54588
    assert result.teams[0].id == 6992
    assert len(result.teams_disbanded) == 0
    assert result.volume.id == 18216


def test_issue_fail(comicvine):
    """Test for a non-existent issue."""
    with pytest.raises(APIError):
        comicvine.issue(-1)


def test_issue_bad_cover_date(comicvine):
    """Test for issue with a cover date."""
    xmen_2 = comicvine.issue(6787)
    assert xmen_2.store_date is None
    assert xmen_2.cover_date == date(1963, 11, 1)
    assert xmen_2.id == 6787
    assert xmen_2.number == "2"
    assert len(xmen_2.creators) == 4
    assert xmen_2.creators[0].name == "Jack Kirby"
    assert xmen_2.creators[0].roles == "penciler"
    assert len(xmen_2.characters) == 10
    assert xmen_2.characters[0].name == "Angel"


def test_issue_list(comicvine):
    """Test the IssueList."""
    search_results = comicvine.issue_list({"filter": f"volume:{VOLUME_ID},issue_number:{NUMBER}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.cover_date == COVER_DATE
    assert result.id == ID
    assert result.name == NAME
    assert result.number == NUMBER
    assert result.store_date == STORE_DATE
    assert result.volume.id == VOLUME_ID


def test_issue_list_empty(comicvine):
    """Test the IssueList with no results."""
    results = comicvine.issue_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_issue_no_has_staff_review(comicvine):
    """Test issue that has staff review data."""
    result = comicvine.issue(505513)
    assert "has_staff_review" not in result.__dict__.keys()


def test_issue_list_no_has_staff_review(comicvine):
    """Test IssueList that has staff review data."""
    result = comicvine.issue_list({"filter": "issue_number:1,volume:85930"})
    assert "has_staff_review" not in result.__dict__.keys()
