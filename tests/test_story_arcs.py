"""
The Test Story Arcs module.

This module contains tests for Story Arc objects.
"""
import pytest

from simyan.exceptions import APIError

FIRST_ISSUE_ID = 155207
ID = 55766
ISSUE_COUNT = 0
NAME = "Blackest Night"
PUBLISHER_ID = 10


def test_story_arc(comicvine):
    """Test for known arcs."""
    result = comicvine.story_arc(ID)
    assert result.first_issue.id == FIRST_ISSUE_ID
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.issues[0].id == 155207
    assert result.name == NAME
    assert result.publisher.id == PUBLISHER_ID


def test_story_arc_fail(comicvine):
    """Test for bad arc requests."""
    with pytest.raises(APIError):
        comicvine.story_arc(-1)


def test_story_arc_list(comicvine):
    """Test for StoryArcList."""
    search_results = comicvine.story_arc_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.first_issue.id == FIRST_ISSUE_ID
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.name == NAME
    assert result.publisher.id == PUBLISHER_ID


def test_story_arc_list_empty(comicvine):
    """Test StoryArcList with no results."""
    results = comicvine.story_arc_list({"filter": "name:INVALID"})
    assert len(results) == 0
