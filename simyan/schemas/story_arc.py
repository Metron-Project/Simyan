"""
The StoryArc module.

This module provides the following classes:

- StoryArc
- StoryArcEntry
"""
__all__ = ["StoryArc", "StoryArcEntry"]
import re
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


class StoryArc(BaseModel):
    r"""
    The StoryArc object contains information for a story arc.

    Attributes:
        aliases: List of names used by the StoryArc, separated by `~\r\n`.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the StoryArc was added.
        date_last_updated: Date and time when the StoryArc was last updated.
        description: Long description of the StoryArc.
        first_issue: First issue of the StoryArc.
        story_arc_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the StoryArc.
        issue_count: Number of issues in the StoryArc.
        issues: List of issues in the StoryArc.
        name: Name/Title of the StoryArc.
        publisher: The publisher of the StoryArc.
        site_url: Url to the resource in Comicvine.
        summary: Short description of the StoryArc.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = Field(default=None, alias="first_appeared_in_issue")
    story_arc_id: int = Field(alias="id")
    image: ImageEntry
    issue_count: int = Field(alias="count_of_isssue_appearances")
    issues: List[GenericEntry] = Field(default_factory=list)
    name: str
    publisher: Optional[GenericEntry] = None
    site_url: str = Field(alias="site_detail_url")
    summary: Optional[str] = Field(default=None, alias="deck")

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the StoryArc has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []


class StoryArcEntry(BaseModel):
    r"""
    The StoryArcEntry object contains information for a story arc.

    Attributes:
        aliases: List of names used by the StoryArcEntry, separated by `~\r\n`.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the StoryArcEntry was added.
        date_last_updated: Date and time when the StoryArcEntry was last updated.
        description: Long description of the StoryArcEntry.
        first_issue: First issue of the StoryArcEntry.
        story_arc_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the StoryArcEntry.
        issue_count: Number of issues in the StoryArcEntry.
        name: Name/Title of the StoryArcEntry.
        publisher: The publisher of the StoryArcEntry.
        site_url: Url to the resource in Comicvine.
        summary: Short description of the StoryArcEntry.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = Field(default=None, alias="first_appeared_in_issue")
    story_arc_id: int = Field(alias="id")
    image: ImageEntry
    issue_count: int = Field(alias="count_of_isssue_appearances")
    name: str
    publisher: Optional[GenericEntry] = None
    site_url: str = Field(alias="site_detail_url")
    summary: Optional[str] = Field(default=None, alias="deck")

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the StoryArcEntry has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []
