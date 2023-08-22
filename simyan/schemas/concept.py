"""The Concept module.

This module provides the following classes:

- Concept
- ConceptEntry
"""
__all__ = ["Concept", "ConceptEntry"]
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, Image, IssueEntry


class BaseConcept(BaseModel):
    r"""Contains fields for all Concepts.

    Attributes:
        aliases: List of names used by the Concept, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Concept was added.
        date_last_updated: Date and time when the Concept was last updated.
        description: Long description of the Concept.
        first_issue: First issue this concept appears.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Concept.
        issue_count: Number of issues with the Concept.
        name: Name/Title of the Concept.
        site_url: Url to the resource in Comicvine.
        start_year: Year the Concept first appeared.
        summary: Short description of the Concept.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = Field(alias="first_appeared_in_issue", default=None)
    id: int  # noqa: A003
    image: Image
    issue_count: int = Field(alias="count_of_isssue_appearances")
    name: str
    site_url: str = Field(alias="site_detail_url")
    start_year: Optional[int] = None
    summary: Optional[str] = Field(alias="deck", default=None)


class Concept(BaseConcept):
    r"""Extends BaseConcept by including all the list references of a concept.

    Attributes:
        issues: List of issues the Concept appears.
        volumes: List of volumes the Concept appears.
    """

    issues: List[IssueEntry] = Field(alias="issue_credits", default_factory=list)
    volumes: List[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class ConceptEntry(BaseConcept):
    """Contains all the fields available when viewing a list of Concepts."""
