"""
The Story Arcs test module.

This module contains tests for Story Arc objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.story_arc import StoryArc


def test_story_arc(session: Comicvine):
    """Test using the story_arc endpoint with a valid story_arc_id."""
    result = session.story_arc(story_arc_id=55766)
    assert result is not None
    assert result.story_arc_id == 55766

    assert result.alias_list == []
    assert result.api_url == "https://comicvine.gamespot.com/api/story_arc/4045-55766/"
    assert result.date_added == datetime(2008, 12, 6, 21, 29, 2)
    assert result.first_issue.id_ == 155207
    assert result.issue_count == 0
    assert len(result.issues) == 86
    assert result.name == "Blackest Night"
    assert result.publisher.id_ == 10
    assert result.site_url == "https://comicvine.gamespot.com/blackest-night/4045-55766/"


def test_story_arc_fail(session: Comicvine):
    """Test using the story_arc endpoint with an invalid story_arc_id."""
    with pytest.raises(ServiceError):
        session.story_arc(story_arc_id=-1)


def test_story_arc_list(session: Comicvine):
    """Test using the story_arc_list endpoint with a valid search."""
    search_results = session.story_arc_list({"filter": "name:Blackest Night"})
    assert len(search_results) != 0
    result = [x for x in search_results if x.story_arc_id == 55766][0]
    assert result is not None

    assert result.alias_list == []
    assert result.api_url == "https://comicvine.gamespot.com/api/story_arc/4045-55766/"
    assert result.date_added == datetime(2008, 12, 6, 21, 29, 2)
    assert result.first_issue.id_ == 155207
    assert result.issue_count == 0
    assert result.issues == []
    assert result.name == "Blackest Night"
    assert result.publisher.id_ == 10
    assert result.site_url == "https://comicvine.gamespot.com/blackest-night/4045-55766/"


def test_story_arc_list_empty(session: Comicvine):
    """Test using the story_arc_list endpoint with an invalid search."""
    results = session.story_arc_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_story_arc_list_max_results(session: Comicvine):
    """Test story_arc_list endpoint with max_results."""
    results = session.story_arc_list({"filter": "name:Night"}, max_results=10)
    assert len(results) == 10


def test_search_story_arc(session: Comicvine):
    """Test using the search endpoint for a list of Story Arcs."""
    results = session.search(resource=ComicvineResource.STORY_ARC, query="Blackest Night")
    assert all(isinstance(x, StoryArc) for x in results)


def test_search_story_arc_max_results(session: Comicvine):
    """Test search endpoint with max_results."""
    results = session.search(
        resource=ComicvineResource.STORY_ARC, query="Blackest Night", max_results=10
    )
    assert all(isinstance(x, StoryArc) for x in results)
    assert len(results) == 0
