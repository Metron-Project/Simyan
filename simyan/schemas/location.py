"""
The Location module.

This module provides the following classes:

- Location
- LocationEntry
"""
__all__ = ["Location", "LocationEntry"]

import re
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


class Location(BaseModel):
    r"""
    The Location object contains information for a location.

    Attributes:
        aliases: List of names used by the Location, separated by `~\r\n`.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Location was added.
        date_last_updated: Date and time when the Location was last updated.
        description: Long description of the Location.
        first_issue: First issue the Location appeared in.
        image: Different sized images, posters and thumbnails for the Location.
        issue_count: Number of issues the Location appears in.
        issues: List of issues the Location appears in.
        location_id: Identifier used by Comicvine.
        name: Name/Title of the Location.
        site_url: Url to the resource in Comicvine.
        start_year: The year the Location was first used.
        story_arcs: List of story arcs the Location appears in.
        summary: Short description of the Location.
        volumes: List of volumes the Location appears in.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = Field(default=None, alias="first_appeared_in_issue")
    image: ImageEntry
    issue_count: int = Field(alias="count_of_issue_appearances")
    issues: List[IssueEntry] = Field(default_factory=list, alias="issue_credits")
    location_id: int = Field(alias="id")
    name: str
    site_url: str = Field(alias="site_detail_url")
    start_year: Optional[int] = None
    story_arcs: List[GenericEntry] = Field(default_factory=list, alias="story_arc_credits")
    summary: Optional[str] = Field(default=None, alias="deck")
    volumes: List[GenericEntry] = Field(default_factory=list, alias="volume_credits")

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Location has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []


class LocationEntry(BaseModel):
    r"""
    The LocationEntry object contains information for a location.

    Attributes:
        aliases: List of names used by the LocationEntry, separated by `~\r\n`.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the LocationEntry was added.
        date_last_updated: Date and time when the LocationEntry was last updated.
        description: Long description of the LocationEntry.
        first_issue: First issue the LocationEntry appeared in.
        image: Different sized images, posters and thumbnails for the LocationEntry.
        issue_count: Number of issues the LocationEntry appears in.
        location_id: Identifier used by Comicvine.
        name: Name/Title of the LocationEntry.
        site_url: Url to the resource in Comicvine.
        start_year: The year the LocationEntry was first used.
        summary: Short description of the LocationEntry.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = Field(default=None, alias="first_appeared_in_issue")
    image: ImageEntry
    issue_count: int = Field(alias="count_of_issue_appearances")
    location_id: int = Field(alias="id")
    name: str
    site_url: str = Field(alias="site_detail_url")
    start_year: Optional[int] = None
    summary: Optional[str] = Field(default=None, alias="deck")

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the LocationEntry has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []
