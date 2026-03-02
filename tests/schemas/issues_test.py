from datetime import date, datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.issue import BasicIssue


def test_get_issue(session: Comicvine) -> None:
    result = session.get_issue(issue_id=111265)
    assert result is not None
    assert result.id == 111265

    assert len(result.characters) == 7
    assert len(result.concepts) == 1
    assert len(result.creators) == 10
    assert len(result.deaths) == 0
    assert len(result.first_appearance_characters) == 0
    assert len(result.first_appearance_concepts) == 0
    assert len(result.first_appearance_locations) == 0
    assert len(result.first_appearance_objects) == 0
    assert len(result.first_appearance_story_arcs) == 0
    assert len(result.first_appearance_teams) == 0
    assert len(result.locations) == 4
    assert len(result.objects) == 1
    assert len(result.story_arcs) == 1
    assert len(result.teams) == 2
    assert len(result.teams_disbanded) == 0


def test_get_issue_fail(session: Comicvine) -> None:
    with pytest.raises(ServiceError):
        session.get_issue(issue_id=-1)


def test_list_issues(session: Comicvine) -> None:
    search_results = session.list_issues({"filter": "volume:18216,issue_number:1"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 111265)
    assert result is not None

    assert len(result.associated_images) == 1
    assert str(result.api_url) == "https://comicvine.gamespot.com/api/issue/4000-111265/"
    assert result.cover_date == date(2005, 7, 1)
    assert result.date_added == datetime(2008, 6, 6, 11, 21, 45)
    assert result.name == "Airborne"
    assert result.number == "1"
    assert (
        str(result.site_url)
        == "https://comicvine.gamespot.com/green-lantern-1-airborne/4000-111265/"
    )
    assert result.store_date == date(2005, 5, 25)
    assert result.volume.id == 18216


def test_list_issues_empty(session: Comicvine) -> None:
    results = session.list_issues({"filter": "name:Invalid Issue Name"})
    assert len(results) == 0


def test_list_issues_max_results(session: Comicvine) -> None:
    results = session.list_issues(max_results=10)
    assert len(results) == 10


def test_search_issue(session: Comicvine) -> None:
    results = session.search(resource=ComicvineResource.ISSUE, query="Lantern")
    assert all(isinstance(x, BasicIssue) for x in results)
