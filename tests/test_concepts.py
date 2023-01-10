"""
The Concepts test module.

This module contains tests for Concept and ConceptEntry objects.
"""
from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.exceptions import ServiceError
from simyan.schemas.concept import ConceptEntry


def test_concept(session: Comicvine):
    """Test using the concept endpoint with a valid concept_id."""
    result = session.concept(concept_id=41148)
    assert result is not None
    assert result.concept_id == 41148

    assert result.alias_list == []
    assert result.api_url == "https://comicvine.gamespot.com/api/concept/4015-41148/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 52)
    assert result.first_issue.id_ == 144069
    assert result.issue_count == 2372
    assert len(result.issues) == 2372
    assert result.name == "Green Lantern"
    assert result.site_url == "https://comicvine.gamespot.com/green-lantern/4015-41148/"
    assert result.start_year == 1940
    assert len(result.volumes) == 1


def test_concept_fail(session: Comicvine):
    """Test using the concept endpoint with an invalid concept_id."""
    with pytest.raises(ServiceError):
        session.concept(concept_id=-1)


def test_concept_list(session: Comicvine):
    """Test using the concept_list endpoint with a valid search."""
    search_results = session.concept_list({"filter": "name:Green Lantern"})
    assert len(search_results) != 0
    result = [x for x in search_results if x.concept_id == 41148][0]
    assert result is not None

    assert result.alias_list == []
    assert result.api_url == "https://comicvine.gamespot.com/api/concept/4015-41148/"
    assert result.date_added == datetime(2008, 6, 6, 11, 27, 52)
    assert result.first_issue.id_ == 144069
    assert result.issue_count == 2372
    assert result.name == "Green Lantern"
    assert result.site_url == "https://comicvine.gamespot.com/green-lantern/4015-41148/"
    assert result.start_year == 1940


def test_concept_list_empty(session: Comicvine):
    """Test using the concept_list endpoint with an invalid search."""
    results = session.concept_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_concept_list_max_results(session: Comicvine):
    """Test concept_list endpoint with max_results."""
    results = session.concept_list(max_results=10)
    assert len(results) == 10


def test_search_concept(session: Comicvine):
    """Test using the search endpoint for a list of Concepts."""
    results = session.search(resource=ComicvineResource.CONCEPT, query="earth")
    assert all(isinstance(x, ConceptEntry) for x in results)


def test_search_concept_max_results(session: Comicvine):
    """Test search endpoint with max_results."""
    results = session.search(resource=ComicvineResource.CONCEPT, query="earth", max_results=10)
    assert all(isinstance(x, ConceptEntry) for x in results)
    assert len(results) == 10
