"""
The Characters test module.

This module contains tests for Character and CharacterEntry objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.character import CharacterEntry


def test_character(session: Comicvine):
    """Test using the character endpoint with a valid character_id."""
    result = session.character(character_id=40431)
    assert result is not None
    assert result.character_id == 40431

    assert result.alias_list == [
        "Green Lantern",
        "Ion",
        "Parallax",
        "Torch Bearer",
        "White Lantern",
        "Green Man",
        "Omega Lantern",
    ]
    assert result.api_url == "https://comicvine.gamespot.com/api/character/4005-40431/"
    assert len(result.creators) == 2
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 42)
    assert result.date_of_birth is None
    assert len(result.deaths) == 2
    assert len(result.enemies) == 146
    assert len(result.enemy_teams) == 24
    assert result.first_issue.id_ == 38445
    assert len(result.friendly_teams) == 16
    assert len(result.friends) == 232
    assert result.gender == 1
    assert result.issue_count == 1565
    assert len(result.issues) == 1565
    assert result.name == "Kyle Rayner"
    assert result.origin.id_ == 4
    assert len(result.powers) == 28
    assert result.publisher.id_ == 10
    assert result.real_name == "Kyle Rayner"
    assert result.site_url == "https://comicvine.gamespot.com/kyle-rayner/4005-40431/"
    assert len(result.story_arcs) == 0
    assert len(result.teams) == 21
    assert len(result.volumes) == 1


def test_character_fail(session: Comicvine):
    """Test using the character endpoint with an invalid character_id."""
    with pytest.raises(ServiceError):
        session.character(character_id=-1)


def test_character_list(session: Comicvine):
    """Test using the character_list endpoint with a valid search."""
    search_results = session.character_list({"filter": "name:Kyle Rayner"})
    assert len(search_results) != 0
    result = [x for x in search_results if x.character_id == 40431][0]
    assert result is not None

    assert result.alias_list == [
        "Green Lantern",
        "Ion",
        "Parallax",
        "Torch Bearer",
        "White Lantern",
        "Green Man",
        "Omega Lantern",
    ]
    assert result.api_url == "https://comicvine.gamespot.com/api/character/4005-40431/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 42)
    assert result.date_of_birth is None
    assert result.first_issue.id_ == 38445
    assert result.gender == 1
    assert result.issue_count == 1565
    assert result.name == "Kyle Rayner"
    assert result.origin.id_ == 4
    assert result.publisher.id_ == 10
    assert result.real_name == "Kyle Rayner"
    assert result.site_url == "https://comicvine.gamespot.com/kyle-rayner/4005-40431/"


def test_character_list_empty(session: Comicvine):
    """Test using the character_list endpoint with an invalid search."""
    results = session.character_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_character_list_max_results(session: Comicvine):
    """Test character_list endpoint with max_results."""
    results = session.character_list({"filter": "name:Kyle"}, max_results=10)
    assert len(results) == 10


def test_search_character(session: Comicvine):
    """Test using the search endpoint for a list of Characters."""
    results = session.search(resource=ComicvineResource.CHARACTER, query="Kyle Rayner")
    assert all(isinstance(x, CharacterEntry) for x in results)


def test_search_character_max_results(session: Comicvine):
    """Test search endpoint with max_results."""
    results = session.search(
        resource=ComicvineResource.CHARACTER, query="Kyle Rayner", max_results=10
    )
    assert all(isinstance(x, CharacterEntry) for x in results)
    assert len(results) == 10
