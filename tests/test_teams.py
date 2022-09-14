"""
The Teams test module.

This module contains tests for Team and TeamEntry objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.team import TeamEntry


def test_team(session: Comicvine):
    """Test using the team endpoint with a valid team_id."""
    result = session.team(team_id=50163)
    assert result is not None
    assert result.team_id == 50163

    assert result.alias_list == []
    assert result.api_url == "https://comicvine.gamespot.com/api/team/4060-50163/"
    assert len(result.enemies) == 5
    assert len(result.friends) == 10
    assert len(result.members) == 17
    assert result.issue_count == 0
    assert result.member_count == 17
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 45)
    assert len(result.issues_disbanded_in) == 1
    assert result.first_issue.id_ == 119950
    assert len(result.issues) == 116
    assert result.name == "Blue Lantern Corps"
    assert result.publisher.id_ == 10
    assert result.site_url == "https://comicvine.gamespot.com/blue-lantern-corps/4060-50163/"
    assert len(result.story_arcs) == 0
    assert len(result.volumes) == 63


def test_team_fail(session: Comicvine):
    """Test using the team endpoint with an invalid team_id."""
    with pytest.raises(ServiceError):
        session.team(team_id=-1)


def test_team_list(session: Comicvine):
    """Test using the team_list endpoint with a valid search."""
    search_results = session.team_list({"filter": "name:Blue Lantern Corps"})
    assert len(search_results) != 0
    result = [x for x in search_results if x.team_id == 50163][0]
    assert result is not None

    assert result.alias_list == []
    assert result.api_url == "https://comicvine.gamespot.com/api/team/4060-50163/"
    assert result.issue_count == 0
    assert result.member_count == 17
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 45)
    assert result.first_issue.id_ == 119950
    assert result.name == "Blue Lantern Corps"
    assert result.publisher.id_ == 10
    assert result.site_url == "https://comicvine.gamespot.com/blue-lantern-corps/4060-50163/"


def test_team_list_empty(session: Comicvine):
    """Test using the team_list endpoint with an invalid search."""
    results = session.team_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_team_list_max_results(session: Comicvine):
    """Test team_list endpoint with max_results."""
    results = session.team_list({"filter": "name:Lantern"}, max_results=10)
    assert len(results) == 10


def test_search_team(session: Comicvine):
    """Test using the search endpoint for a list of Teams."""
    results = session.search(resource=ComicvineResource.TEAM, query="Lantern")
    assert all(isinstance(x, TeamEntry) for x in results)


def test_search_team_max_results(session: Comicvine):
    """Test search endpoint with max_results."""
    results = session.search(resource=ComicvineResource.TEAM, query="Lantern", max_results=10)
    assert all(isinstance(x, TeamEntry) for x in results)
    assert len(results) == 10
