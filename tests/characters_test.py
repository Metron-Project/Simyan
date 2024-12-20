"""The Characters test module.

This module contains tests for Character and BasicCharacter objects.
"""

from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.character import BasicCharacter


def test_get_character(session: Comicvine) -> None:
    """Test the get_character function with a valid id."""
    result = session.get_character(character_id=40431)
    assert result is not None
    assert result.id == 40431

    assert len(result.creators) == 2
    assert len(result.deaths) == 2
    assert len(result.enemies) == 150
    assert len(result.enemy_teams) == 25
    assert len(result.friendly_teams) == 17
    assert len(result.friends) == 233
    assert len(result.issues) == 1714
    assert len(result.powers) == 28
    assert len(result.story_arcs) == 0
    assert len(result.teams) == 21
    assert len(result.volumes) == 1


def test_get_character_fail(session: Comicvine) -> None:
    """Test the get_character function with an invalid id."""
    with pytest.raises(ServiceError):
        session.get_character(character_id=-1)


def test_list_characters(session: Comicvine) -> None:
    """Test the list_characters function with a valid search."""
    search_results = session.list_characters({"filter": "name:Kyle Rayner"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 40431)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/character/4005-40431/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 42)
    assert result.date_of_birth is None
    assert result.first_issue.id == 38445
    assert result.gender == 1
    assert result.issue_count == 1714
    assert result.name == "Kyle Rayner"
    assert result.origin.id == 4
    assert result.publisher.id == 10
    assert result.real_name == "Kyle Rayner"
    assert str(result.site_url) == "https://comicvine.gamespot.com/kyle-rayner/4005-40431/"


def test_list_characters_empty(session: Comicvine) -> None:
    """Test the list_characters function with an invalid search."""
    results = session.list_characters({"filter": "name:INVALID"})
    assert len(results) == 0


def test_list_characters_max_results(session: Comicvine) -> None:
    """Test the list_characters function with max_results."""
    results = session.list_characters(max_results=10)
    assert len(results) == 10


def test_search_character(session: Comicvine) -> None:
    """Test the search function for a list of Characters."""
    results = session.search(resource=ComicvineResource.CHARACTER, query="Kyle Rayner")
    assert all(isinstance(x, BasicCharacter) for x in results)
