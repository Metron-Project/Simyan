"""The StoryArc module.

This module provides the following classes:

- StoryArc
- StoryArcEntry
"""
__all__ = ["StoryArc", "StoryArcEntry"]
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, Image, IssueEntry


class BaseStoryArc(BaseModel):
    r"""Contains fields for all Story Arcs.

    Attributes:
        aliases: List of names used by the Story Arc, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Story Arc was added.
        date_last_updated: Date and time when the Story Arc was last updated.
        description: Long description of the Story Arc.
        first_issue: First issue of the Story Arc.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Story Arc.
        issue_count: Number of issues in the Story Arc.
        name: Name/Title of the Story Arc.
        publisher: The publisher of the Story Arc.
        site_url: Url to the resource in Comicvine.
        summary: Short description of the Story Arc.
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
    publisher: Optional[GenericEntry] = None
    site_url: str = Field(alias="site_detail_url")
    summary: Optional[str] = Field(alias="deck", default=None)


class StoryArc(BaseStoryArc):
    r"""Extends BaseStoryArc by including all the list references of a story arc.

    Attributes:
        issues: List of issues in the Story Arc.
    """

    issues: List[GenericEntry] = Field(default_factory=list)


class StoryArcEntry(BaseStoryArc):
    """Contains all the fields available when viewing a list of Story Arcs."""
