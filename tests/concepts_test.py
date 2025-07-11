"""The Concepts test module.

This module contains tests for Concept and BasicConcept objects.
"""

from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.concept import BasicConcept


def test_get_concept(session: Comicvine) -> None:
    """Test the get_concept function with a valid id."""
    result = session.get_concept(concept_id=41148)
    assert result is not None
    assert result.id == 41148

    assert len(result.issues) == 2652
    assert len(result.volumes) == 1


def test_get_concept_fail(session: Comicvine) -> None:
    """Test the get_concept function with an invalid id."""
    with pytest.raises(ServiceError):
        session.get_concept(concept_id=-1)


def test_list_concepts(session: Comicvine) -> None:
    """Test the list_concepts function with a valid search."""
    search_results = session.list_concepts({"filter": "name:Green Lantern"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 41148)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/concept/4015-41148/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 52)
    assert result.first_issue.id == 144069
    assert result.issue_count == 2652
    assert result.name == "Green Lantern"
    assert str(result.site_url) == "https://comicvine.gamespot.com/green-lantern/4015-41148/"
    assert result.start_year == 1940


def test_list_concepts_empty(session: Comicvine) -> None:
    """Test the list_concepts function with an invalid search."""
    results = session.list_concepts({"filter": "name:INVALID"})
    assert len(results) == 0


def test_list_concepts_max_results(session: Comicvine) -> None:
    """Test the list_concepts function with max_results."""
    results = session.list_concepts(max_results=10)
    assert len(results) == 10


def test_search_concept(session: Comicvine) -> None:
    """Test the search function for a list of Concepts."""
    results = session.search(resource=ComicvineResource.CONCEPT, query="earth")
    assert all(isinstance(x, BasicConcept) for x in results)
