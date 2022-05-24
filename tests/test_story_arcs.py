"""
The Test Story Arcs module.

This module contains tests for Story Arc objects.
"""
import pytest

from simyan.comicvine import Comicvine
from simyan.exceptions import APIError

FIRST_ISSUE_ID = 155207
ID = 55766
ISSUE_COUNT = 0
NAME = "Blackest Night"
PUBLISHER_ID = 10


def test_story_arc(session: Comicvine):
    """Test for known arcs."""
    result = session.story_arc(story_arc_id=ID)
    assert result.first_issue.id_ == FIRST_ISSUE_ID
    assert result.id_ == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.issues[0].id_ == 155207
    assert result.name == NAME
    assert result.publisher.id_ == PUBLISHER_ID


def test_story_arc_fail(session: Comicvine):
    """Test for bad arc requests."""
    with pytest.raises(APIError):
        session.story_arc(story_arc_id=-1)


def test_story_arc_list(session: Comicvine):
    """Test for StoryArcList."""
    search_results = session.story_arc_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id_ == ID][0]
    assert result.first_issue.id_ == FIRST_ISSUE_ID
    assert result.id_ == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.name == NAME
    assert result.publisher.id_ == PUBLISHER_ID


def test_story_arc_list_empty(session: Comicvine):
    """Test StoryArcList with no results."""
    results = session.story_arc_list({"filter": "name:INVALID"})
    assert len(results) == 0
