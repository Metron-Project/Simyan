"""The Teams test module.

This module contains tests for Team and BasicTeam objects.
"""

from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.team import BasicTeam


def test_get_team(session: Comicvine) -> None:
    """Test the get_team function with a valid id."""
    result = session.get_team(team_id=50163)
    assert result is not None
    assert result.id == 50163

    assert len(result.enemies) == 5
    assert len(result.friends) == 10
    assert len(result.issues) == 120
    assert len(result.issues_disbanded_in) == 1
    assert len(result.members) == 18
    assert len(result.story_arcs) == 0
    assert len(result.volumes) == 65


def test_get_team_fail(session: Comicvine) -> None:
    """Test the get_team function with an invalid id."""
    with pytest.raises(ServiceError):
        session.get_team(team_id=-1)


def test_list_teams(session: Comicvine) -> None:
    """Test the list_teams function with a valid search."""
    search_results = session.list_teams({"filter": "name:Blue Lantern Corps"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 50163)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/team/4060-50163/"
    assert result.issue_count == 0
    assert result.member_count == 18
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 45)
    assert result.first_issue.id == 119950
    assert result.name == "Blue Lantern Corps"
    assert result.publisher.id == 10
    assert str(result.site_url) == "https://comicvine.gamespot.com/blue-lantern-corps/4060-50163/"


def test_list_teams_empty(session: Comicvine) -> None:
    """Test the list_teams function with an invalid search."""
    results = session.list_teams({"filter": "name:INVALID"})
    assert len(results) == 0


def test_list_teams_max_results(session: Comicvine) -> None:
    """Test the list_teams function with max_results."""
    results = session.list_teams(max_results=10)
    assert len(results) == 10


def test_search_team(session: Comicvine) -> None:
    """Test the search endpoint for a list of Teams."""
    results = session.search(resource=ComicvineResource.TEAM, query="Lantern")
    assert all(isinstance(x, BasicTeam) for x in results)
