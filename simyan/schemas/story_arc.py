"""
The StoryArc module.

This module provides the following classes:

- StoryArc
"""
__all__ = ["StoryArc"]
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
        aliases: List of names used by the Story Arc, separated by `~\\r\\n`.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Story Arc was added.
        date_last_updated: Date and time when the Story Arc was last updated.
        description: Long description of the Story Arc.
        first_issue: First issue of the Story Arc.
        id_: Identifier used by Comicvine. **Deprecated:** Use story_arc_id instead.
        story_arc_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Story Arc.
        issue_count: Number of issues in the Story Arc.
        issues: List of issues in the Story Arc.
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
    first_issue: Optional[IssueEntry] = Field(default=None, alias="first_appeared_in_issue")
    id_: int = Field(alias="id")
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
        List of aliases the Story Arc has used.

        Returns:
            List of aliases, split by `~\\r\\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []
