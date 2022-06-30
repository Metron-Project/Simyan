"""
The StoryArc module.

This module provides the following classes:

- StoryArc
"""
import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


class StoryArc(BaseModel):
    """The StoryArc object contains information for a story arc."""

    aliases: Optional[str] = Field(
        default=None
    )  #: List of names the Story Arc has used, separated by ``\n``.
    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    date_added: datetime  #: Date and time when the Story Arc was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Story Arc was updated on Comicvine.
    description: Optional[str] = Field(default=None)  #: Long description of the Story Arc.
    first_issue: IssueEntry = Field(
        alias="first_appeared_in_issue"
    )  #: First issue of the Story Arc.
    id_: int = Field(alias="id")  #: Identifier used in Comicvine.
    story_arc_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Story Arc.
    issue_count: int = Field(
        alias="count_of_isssue_appearances"
    )  #: Number of issues in the Story Arc.
    issues: List[GenericEntry] = Field(default_factory=list)  #: List of issues in the Story Arc.
    name: str  #: Name/Title of the Story Arc.
    publisher: GenericEntry  #: The publisher of the Story Arc.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    summary: Optional[str] = Field(
        default=None, alias="deck"
    )  #: Short description of the Story Arc.

    @property
    def alias_list(self) -> List[str]:
        """List of names the Story Arc has used."""
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.ignore
