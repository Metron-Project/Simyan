"""
The StoryArc module.

This module provides the following classes:

- StoryArc
- StoryArcResult
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


class StoryArc(BaseModel):
    """The StoryArc object contains information for a story arc."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    date_added: datetime  #: Date and time when the Story Arc was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Story Arc was updated on Comicvine.
    first_issue: IssueEntry = Field(
        alias="first_appeared_in_issue"
    )  #: First issue of the Story Arc.
    id_: int = Field(
        alias="id"
    )  #: Identifier used in Comicvine *Deprecated use story_arc_id instead*.
    story_arc_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Story Arc.
    issue_count: int = Field(
        alias="count_of_isssue_appearances"
    )  #: Number of issues in the Story Arc.
    name: str  #: Name/Title of the Story Arc.
    publisher: GenericEntry  #: The publisher of the Story Arc.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    aliases: Optional[str] = None  #: List of names the Story Arc has used, separated by ``\n``.
    description: Optional[str] = None  #: Long description of the Story Arc.
    issues: List[GenericEntry] = Field(default_factory=list)  #: List of issues in the Story Arc.
    summary: Optional[str] = Field(
        default=None, alias="deck"
    )  #: Short description of the Story Arc.


class StoryArcResult(BaseModel):
    """The StoryArcResult object contains information for a story arc."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    date_added: datetime  #: Date and time when the Story Arc was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Story Arc was updated on Comicvine.
    first_issue: IssueEntry = Field(
        alias="first_appeared_in_issue"
    )  #: First issue of the Story Arc.
    id_: int = Field(
        alias="id"
    )  #: Identifier used in Comicvine *Deprecated use story_arc_id instead*.
    story_arc_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Story Arc.
    issue_count: int = Field(
        alias="count_of_isssue_appearances"
    )  #: Number of issues in the Story Arc.
    name: str  #: Name/Title of the Story Arc.
    publisher: GenericEntry  #: The publisher of the Story Arc.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    aliases: Optional[str] = None  #: List of names the Story Arc has used, separated by ``\n``.
    description: Optional[str] = None  #: Long description of the Story Arc.
    summary: Optional[str] = Field(
        default=None, alias="deck"
    )  #: Short description of the Story Arc.
