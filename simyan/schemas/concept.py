"""
The Concept module.

This module provides the following classes:

- Concept
- ConceptEntry
"""
__all__ = ["Concept", "ConceptEntry"]
import re
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


class BaseConcept(BaseModel):
    r"""
    Contains fields for all Concepts.

    Attributes:
        aliases: List of names used by the Concept, separated by `~\r\n`.
        api_url: Url to the resource in the Comicvine API.
        concept_id: Identifier used by Comicvine.
        date_added: Date and time when the Concept was added.
        date_last_updated: Date and time when the Concept was last updated.
        description: Long description of the Concept.
        first_issue: First issue this concept appears.
        image: Different sized images, posters and thumbnails for the Concept.
        issue_count: Number of issues with the Concept.
        name: Name/Title of the Concept.
        site_url: Url to the resource in Comicvine.
        start_year: Year the Concept first appeared.
        summary: Short description of the Concept.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    concept_id: int = Field(alias="id")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = Field(alias="first_appeared_in_issue", default=None)
    image: ImageEntry
    issue_count: int = Field(alias="count_of_isssue_appearances")
    name: str
    site_url: str = Field(alias="site_detail_url")
    start_year: Optional[int] = None
    summary: Optional[str] = Field(alias="deck", default=None)

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Concept has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []


class Concept(BaseConcept):
    r"""
    Extends BaseConcept by including all the list references of a concept.

    Attributes:
        issues: List of issues the Concept appears.
        volumes: List of volumes the Concept appears.
    """

    issues: List[IssueEntry] = Field(alias="issue_credits", default_factory=list)
    volumes: List[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class ConceptEntry(BaseConcept):
    """Contains all the fields available when viewing a list of Concepts."""
