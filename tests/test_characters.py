"""
The Test Characters module.

This module contains tests for Character objects.
"""
import pytest

from simyan.comicvine import Comicvine
from simyan.exceptions import APIError

DATE_OF_BIRTH = None
FIRST_ISSUE_ID = 38445
GENDER = 1
ID = 40431
ISSUE_COUNT = 1557
NAME = "Kyle Rayner"
ORIGIN_ID = 4
PUBLISHER_ID = 10
REAL_NAME = "Kyle Rayner"


def test_character(session: Comicvine):
    """Test for a known character."""
    result = session.character(character_id=ID)
    assert result.creators[0].id_ == 9569
    assert result.date_of_birth == DATE_OF_BIRTH
    assert result.deaths[0].id_ == 442830
    assert result.enemies[0].id_ == 47300
    assert result.enemy_teams[0].id_ == 20659
    assert result.first_issue.id_ == FIRST_ISSUE_ID
    assert result.friendly_teams[0].id_ == 63877
    assert result.friends[0].id_ == 19067
    assert result.gender == GENDER
    assert result.id_ == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.issues[0].id_ == 895904
    assert result.name == NAME
    assert result.origin.id_ == ORIGIN_ID
    assert result.powers[0].id_ == 1
    assert result.publisher.id_ == PUBLISHER_ID
    assert result.real_name == REAL_NAME
    assert len(result.story_arcs) == 0
    assert result.teams[0].id_ == 50163
    assert result.volumes[0].id_ == 43262


def test_character_fail(session: Comicvine):
    """Test for a non-existent character."""
    with pytest.raises(APIError):
        session.character(character_id=-1)


def test_character_list(session: Comicvine):
    """Test the CharactersList."""
    search_results = session.character_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id_ == ID][0]
    assert result.date_of_birth == DATE_OF_BIRTH
    assert result.first_issue.id_ == FIRST_ISSUE_ID
    assert result.gender == GENDER
    assert result.id_ == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.name == NAME
    assert result.origin.id_ == ORIGIN_ID
    assert result.publisher.id_ == PUBLISHER_ID
    assert result.real_name == REAL_NAME


def test_character_list_empty(session: Comicvine):
    """Test CharacterList with bad response."""
    results = session.character_list({"filter": "name:INVALID"})
    assert len(results) == 0
