from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.story_arc import BasicStoryArc


def test_get_story_arc(session: Comicvine) -> None:
    result = session.get_story_arc(story_arc_id=55766)
    assert result is not None
    assert result.id == 55766

    assert len(result.issues) == 86


def test_get_story_arc_fail(session: Comicvine) -> None:
    with pytest.raises(ServiceError):
        session.get_story_arc(story_arc_id=-1)


def test_list_story_arcs(session: Comicvine) -> None:
    results = session.list_story_arcs({"filter": "name:Blackest Night"})
    assert len(results) != 0
    result = next(x for x in results if x.id == 55766)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/story_arc/4045-55766/"
    assert result.date_added == datetime(2008, 12, 6, 21, 29, 2)
    assert result.first_issue.id == 155207
    assert result.issue_count == 0
    assert result.name == '"Green Lantern" Blackest Night'
    assert result.publisher.id == 10
    assert (
        str(result.site_url)
        == "https://comicvine.gamespot.com/green-lantern-blackest-night/4045-55766/"
    )


def test_list_story_arcs_empty(session: Comicvine) -> None:
    results = session.list_story_arcs({"filter": "name:Invalid StoryArc Name"})
    assert len(results) == 0


def test_list_story_arcs_max_results(session: Comicvine) -> None:
    results = session.list_story_arcs(max_results=10)
    assert len(results) == 10


def test_search_story_arc(session: Comicvine) -> None:
    results = session.search(resource=ComicvineResource.STORY_ARC, query="Blackest Night")
    assert all(isinstance(x, BasicStoryArc) for x in results)
