"""The Story Arcs test module.

This module contains tests for StoryArc and StoryArcEntry objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.story_arc import StoryArcEntry


def test_story_arc(session: Comicvine) -> None:
    """Test using the story_arc endpoint with a valid story_arc_id."""
    result = session.get_story_arc(story_arc_id=55766)
    assert result is not None
    assert result.id == 55766

    assert result.api_url == "https://comicvine.gamespot.com/api/story_arc/4045-55766/"
    assert result.date_added.astimezone() == datetime(2008, 12, 6, 21, 29, 2).astimezone()
    assert result.first_issue.id == 155207
    assert result.issue_count == 0
    assert len(result.issues) == 86
    assert result.name == "Blackest Night"
    assert result.publisher.id == 10
    assert result.site_url == "https://comicvine.gamespot.com/blackest-night/4045-55766/"


def test_story_arc_fail(session: Comicvine) -> None:
    """Test using the story_arc endpoint with an invalid story_arc_id."""
    with pytest.raises(ServiceError):
        session.get_story_arc(story_arc_id=-1)


def test_story_arc_null_first_issue(session: Comicvine) -> None:
    """Test story_arc endpoint to return result with no first_issue."""
    result = session.get_story_arc(story_arc_id=56273)
    assert result.first_issue is None


def test_story_arc_null_publisher(session: Comicvine) -> None:
    """Test story_arc endpoint to return result with no publisher."""
    result = session.get_story_arc(story_arc_id=56765)
    assert result.publisher is None


def test_story_arc_list(session: Comicvine) -> None:
    """Test using the story_arc_list endpoint with a valid search."""
    results = session.list_story_arcs({"filter": "name:Blackest Night"})
    assert len(results) != 0
    result = next(x for x in results if x.id == 55766)
    assert result is not None

    assert result.api_url == "https://comicvine.gamespot.com/api/story_arc/4045-55766/"
    assert result.date_added.astimezone() == datetime(2008, 12, 6, 21, 29, 2).astimezone()
    assert result.first_issue.id == 155207
    assert result.issue_count == 0
    assert result.name == "Blackest Night"
    assert result.publisher.id == 10
    assert result.site_url == "https://comicvine.gamespot.com/blackest-night/4045-55766/"


def test_story_arc_list_empty(session: Comicvine) -> None:
    """Test using the story_arc_list endpoint with an invalid search."""
    results = session.list_story_arcs({"filter": "name:INVALID"})
    assert len(results) == 0


def test_story_arc_list_max_results(session: Comicvine) -> None:
    """Test story_arc_list endpoint with max_results."""
    results = session.list_story_arcs({"filter": "name:Night"}, max_results=10)
    assert len(results) == 10


def test_story_arc_list_null_first_issue(session: Comicvine) -> None:
    """Test story_arc_list endpoint to return result with no first_issue."""
    results = session.list_story_arcs({"filter": "name:Lo, this Monster"})
    assert len(results) != 0
    result = next(x for x in results if x.id == 56273)
    assert result is not None
    assert result.first_issue is None


def test_story_arc_list_null_publisher(session: Comicvine) -> None:
    """Test story_arc_list endpoint to return result with no publisher."""
    results = session.list_story_arcs({"filter": "name:Lo, this Monster"})
    assert len(results) != 0
    result = next(x for x in results if x.id == 56765)
    assert result is not None
    assert result.publisher is None


def test_search_story_arc(session: Comicvine) -> None:
    """Test using the search endpoint for a list of Story Arcs."""
    results = session.search(resource=ComicvineResource.STORY_ARC, query="Blackest Night")
    assert all(isinstance(x, StoryArcEntry) for x in results)


def test_search_story_arc_max_results(session: Comicvine) -> None:
    """Test search endpoint with max_results."""
    results = session.search(
        resource=ComicvineResource.STORY_ARC,
        query="Blackest Night",
        max_results=10,
    )
    assert all(isinstance(x, StoryArcEntry) for x in results)
    assert len(results) == 0
