from datetime import datetime

import pytest
from responses import RequestsMock as Mocker
from responses.matchers import query_param_matcher

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.concept import BasicConcept


def test_get_concept(session: Comicvine) -> None:
    result = session.get_concept(concept_id=41148)
    assert result is not None
    assert result.id == 41148

    assert len(result.issues) == 2726
    assert len(result.volumes) == 1


def test_get_concept_fail(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = f"https://comicvine.gamespot.mock/api/concept/{ComicvineResource.CONCEPT.resource_id}--1/"
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params)],
            status=404,
            json={"detail": "Not found."},
        )
        with pytest.raises(ServiceError):
            mock_session.get_concept(concept_id=-1)
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)


def test_list_concepts(session: Comicvine) -> None:
    search_results = session.list_concepts({"filter": "name:Green Lantern"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 41148)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/concept/4015-41148/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 52)
    assert result.first_issue.id == 144069
    assert result.issue_count == 2726
    assert result.name == "Green Lantern"
    assert str(result.site_url) == "https://comicvine.gamespot.com/green-lantern/4015-41148/"
    assert result.start_year == 1940


def test_list_concepts_empty(session: Comicvine) -> None:
    results = session.list_concepts({"filter": "name:Invalid Concept Name"})
    assert len(results) == 0


def test_list_concepts_max_results(session: Comicvine) -> None:
    results = session.list_concepts(max_results=10)
    assert len(results) == 10


def test_search_deprecation(session: Comicvine) -> None:
    with pytest.deprecated_call():
        results = session.search(resource=ComicvineResource.CONCEPT, query="earth")
        assert all(isinstance(x, BasicConcept) for x in results)


def test_search_concept(session: Comicvine) -> None:
    results = session.search_concepts(query="earth")
    assert all(isinstance(x, BasicConcept) for x in results)
