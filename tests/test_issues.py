"""
The Test Issues module.

This module contains tests for Issue objects.
"""
from datetime import date

import pytest

from simyan.comicvine import Comicvine
from simyan.exceptions import APIError

COVER_DATE = date(year=2005, month=7, day=1)
ID = 111265
NAME = "Airborne"
NUMBER = "1"
STORE_DATE = date(year=2005, month=5, day=18)
VOLUME_ID = 18216


def test_issue(session: Comicvine):
    """Test for a known issue."""
    result = session.issue(issue_id=ID)
    assert result.characters[0].id_ == 22634
    assert result.concepts[0].id_ == 41148
    assert result.cover_date == COVER_DATE
    assert result.creators[0].id_ == 10945
    assert len(result.deaths) == 0
    assert result.first_appearance_characters is None
    assert result.first_appearance_concepts is None
    assert result.first_appearance_locations is None
    assert result.first_appearance_objects is None
    assert result.first_appearance_story_arcs is None
    assert result.first_appearance_teams is None
    assert result.id_ == ID
    assert result.locations[0].id_ == 56427
    assert result.name == NAME
    assert result.number == NUMBER
    assert result.objects[0].id_ == 41361
    assert result.store_date == STORE_DATE
    assert result.story_arcs[0].id_ == 54588
    assert result.teams[0].id_ == 6992
    assert len(result.teams_disbanded) == 0
    assert result.volume.id_ == 18216


def test_issue_fail(session: Comicvine):
    """Test for a non-existent issue."""
    with pytest.raises(APIError):
        session.issue(issue_id=-1)


def test_issue_bad_cover_date(session: Comicvine):
    """Test for issue with a cover date."""
    xmen_2 = session.issue(issue_id=6787)
    assert xmen_2.store_date is None
    assert xmen_2.cover_date == date(1963, 11, 1)
    assert xmen_2.id_ == 6787
    assert xmen_2.number == "2"
    assert len(xmen_2.creators) == 4
    assert xmen_2.creators[0].name == "Jack Kirby"
    assert xmen_2.creators[0].roles == "penciler"
    assert len(xmen_2.characters) == 10
    assert xmen_2.characters[0].name == "Angel"


def test_issue_list(session: Comicvine):
    """Test the IssueList."""
    search_results = session.issue_list({"filter": f"volume:{VOLUME_ID},issue_number:{NUMBER}"})
    result = [x for x in search_results if x.id_ == ID][0]
    assert result.cover_date == COVER_DATE
    assert result.id_ == ID
    assert result.name == NAME
    assert result.number == NUMBER
    assert result.store_date == STORE_DATE
    assert result.volume.id_ == VOLUME_ID


def test_issue_list_empty(session: Comicvine):
    """Test the IssueList with no results."""
    results = session.issue_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_issue_no_has_staff_review(session: Comicvine):
    """Test issue that has staff review data."""
    result = session.issue(issue_id=505513)
    assert "has_staff_review" not in result.__dict__.keys()


def test_issue_list_no_has_staff_review(session: Comicvine):
    """Test IssueList that has staff review data."""
    result = session.issue_list({"filter": "issue_number:1,volume:85930"})
    assert "has_staff_review" not in result[0].__dict__.keys()


def test_issue_no_description(session: Comicvine):
    """Test issue that has a null/no description result."""
    result = session.issue(issue_id=134272)
    assert result.description is None


def test_issue_list_no_description(session: Comicvine):
    """Test IssueList that has a null/no description result."""
    results = session.issue_list(params={"filter": "volume:18006"})
    result = [x for x in results if x.id_ == 134272][0]
    assert result.description is None


def test_issue_no_cover_date(session: Comicvine):
    """Test issue that has a null/no cover_date result."""
    result = session.issue(issue_id=325298)
    assert result.cover_date is None


def test_issue_list_no_cover_date(session: Comicvine):
    """Test IssueList that has a null/no cover_date result."""
    results = session.issue_list(params={"filter": "volume:3088"})
    result = [x for x in results if x.id_ == 325298][0]
    assert result.cover_date is None
