from datetime import datetime

import pytest
from responses import RequestsMock as Mocker
from responses.matchers import query_param_matcher

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.character import BasicCharacter


def test_get_character(session: Comicvine) -> None:
    result = session.get_character(character_id=40431)
    assert result is not None
    assert result.id == 40431

    assert len(result.creators) == 2
    assert len(result.deaths) == 2
    assert len(result.enemies) == 154
    assert len(result.enemy_teams) == 28
    assert len(result.friendly_teams) == 18
    assert len(result.friends) == 238
    assert len(result.issues) == 1773
    assert len(result.powers) == 28
    assert len(result.story_arcs) == 0
    assert len(result.teams) == 21
    assert len(result.volumes) == 1


def test_get_character_fail(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = f"https://comicvine.gamespot.mock/api/character/{ComicvineResource.CHARACTER.resource_id}--1/"
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params)],
            status=404,
            json={"detail": "Not found."},
        )
        with pytest.raises(ServiceError):
            mock_session.get_character(character_id=-1)
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)


def test_list_characters(session: Comicvine) -> None:
    search_results = session.list_characters({"filter": "name:Kyle Rayner"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 40431)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/character/4005-40431/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 42)
    assert result.date_of_birth is None
    assert result.first_issue.id == 38445
    assert result.gender == 1
    assert result.issue_count == 1773
    assert result.name == "Kyle Rayner"
    assert result.origin.id == 4
    assert result.publisher.id == 10
    assert result.real_name == "Kyle Rayner"
    assert str(result.site_url) == "https://comicvine.gamespot.com/kyle-rayner/4005-40431/"


def test_list_characters_empty(session: Comicvine) -> None:
    results = session.list_characters({"filter": "name:Invalid Character Name"})
    assert len(results) == 0


def test_list_characters_max_results(session: Comicvine) -> None:
    results = session.list_characters(max_results=10)
    assert len(results) == 10


def test_search_deprecation(session: Comicvine) -> None:
    with pytest.deprecated_call():
        results = session.search(resource=ComicvineResource.CHARACTER, query="Kyle Rayner")
        assert all(isinstance(x, BasicCharacter) for x in results)


def test_search_character(session: Comicvine) -> None:
    results = session.search_characters(query="Kyle Rayner")
    assert all(isinstance(x, BasicCharacter) for x in results)
