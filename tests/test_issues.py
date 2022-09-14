"""
The Issues test module.

This module contains tests for Issue and IssueEntry objects.
"""
from datetime import date, datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.issue import IssueEntry


def test_issue(session: Comicvine):
    """Test using the issue endpoint with a valid issue_id."""
    result = session.issue(issue_id=111265)
    assert result is not None
    assert result.issue_id == 111265

    assert result.alias_list == []
    assert len(result.alternative_images) == 1
    assert result.api_url == "https://comicvine.gamespot.com/api/issue/4000-111265/"
    assert len(result.characters) == 7
    assert len(result.concepts) == 1
    assert result.cover_date == date(2005, 7, 1)
    assert len(result.creators) == 10
    assert result.date_added == datetime(2008, 6, 6, 11, 21, 45)
    assert len(result.deaths) == 0
    assert len(result.first_appearance_characters) == 0
    assert len(result.first_appearance_concepts) == 0
    assert len(result.first_appearance_locations) == 0
    assert len(result.first_appearance_objects) == 0
    assert len(result.first_appearance_story_arcs) == 0
    assert len(result.first_appearance_teams) == 0
    assert len(result.locations) == 4
    assert result.name == "Airborne"
    assert result.number == "1"
    assert len(result.objects) == 1
    assert result.site_url == "https://comicvine.gamespot.com/green-lantern-1-airborne/4000-111265/"
    assert result.store_date == date(2005, 5, 18)
    assert len(result.story_arcs) == 1
    assert len(result.teams) == 2
    assert len(result.teams_disbanded) == 0
    assert result.volume.id_ == 18216


def test_issue_fail(session: Comicvine):
    """Test using the issue endpoint with an invalid issue_id."""
    with pytest.raises(ServiceError):
        session.issue(issue_id=-1)


def test_issue_list(session: Comicvine):
    """Test using the issue_list endpoint with a valid search."""
    search_results = session.issue_list({"filter": "volume:18216,issue_number:1"})
    assert len(search_results) != 0
    result = [x for x in search_results if x.issue_id == 111265][0]
    assert result is not None

    assert result.alias_list == []
    assert len(result.alternative_images) == 1
    assert result.api_url == "https://comicvine.gamespot.com/api/issue/4000-111265/"
    assert result.cover_date == date(2005, 7, 1)
    assert result.date_added == datetime(2008, 6, 6, 11, 21, 45)
    assert result.name == "Airborne"
    assert result.number == "1"
    assert result.site_url == "https://comicvine.gamespot.com/green-lantern-1-airborne/4000-111265/"
    assert result.store_date == date(2005, 5, 18)
    assert result.volume.id_ == 18216


def test_issue_list_empty(session: Comicvine):
    """Test using the issue_list endpoint with an invalid search."""
    results = session.issue_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_issue_list_max_results(session: Comicvine):
    """Test issue_list endpoint with max_results."""
    results = session.issue_list({"filter": "volume:18216"}, max_results=10)
    assert len(results) == 10


def test_search_issue(session: Comicvine):
    """Test using the search endpoint for a list of Issues."""
    results = session.search(resource=ComicvineResource.ISSUE, query="Lantern")
    assert all(isinstance(x, IssueEntry) for x in results)


def test_search_issue_max_results(session: Comicvine):
    """Test search endpoint with max_results."""
    results = session.search(resource=ComicvineResource.ISSUE, query="Lantern", max_results=10)
    assert all(isinstance(x, IssueEntry) for x in results)
    assert len(results) == 10


def test_issue_bad_cover_date(session: Comicvine):
    """Test for issue with a cover date."""
    xmen_2 = session.issue(issue_id=6787)
    assert xmen_2.store_date is None
    assert xmen_2.cover_date == date(1963, 11, 1)
    assert xmen_2.issue_id == 6787
    assert xmen_2.number == "2"
    assert len(xmen_2.creators) == 4
    assert xmen_2.creators[0].name == "Jack Kirby"
    assert xmen_2.creators[0].roles == "penciler"
    assert len(xmen_2.characters) == 10
    assert xmen_2.characters[0].name == "Angel"


def test_issue_no_has_staff_review(session: Comicvine):
    """Test issue endpoint to return result without a Staff Review field."""
    result = session.issue(issue_id=505513)
    assert "has_staff_review" not in result.__dict__.keys()


def test_issue_list_no_has_staff_review(session: Comicvine):
    """Test issue_list endpoint to return result without a Staff Review field."""
    result = session.issue_list({"filter": "issue_number:1,volume:85930"})
    assert "has_staff_review" not in result[0].__dict__.keys()


def test_issue_no_description(session: Comicvine):
    """Test issue endpoint to return result that has a null/no description."""
    result = session.issue(issue_id=134272)
    assert result.description is None


def test_issue_list_no_description(session: Comicvine):
    """Test issue_list endpoint to return result that has a null/no description."""
    results = session.issue_list(params={"filter": "volume:18006"})
    result = [x for x in results if x.issue_id == 134272][0]
    assert result.description is None


def test_issue_no_cover_date(session: Comicvine):
    """Test issue endpoint to return result that has a null/no cover_date."""
    result = session.issue(issue_id=325298)
    assert result.cover_date is None


def test_issue_list_no_cover_date(session: Comicvine):
    """Test issue_list endpoint to return result that has a null/no cover_date."""
    results = session.issue_list(params={"filter": "volume:3088"})
    result = [x for x in results if x.issue_id == 325298][0]
    assert result.cover_date is None
