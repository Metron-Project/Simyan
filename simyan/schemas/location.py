"""The Location module.

This module provides the following classes:

- Location
- LocationEntry
"""
__all__ = ["Location", "LocationEntry"]

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, Image, IssueEntry


class BaseLocation(BaseModel):
    r"""Contains fields for all Locations.

    Attributes:
        aliases: List of names used by the Location, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Location was added.
        date_last_updated: Date and time when the Location was last updated.
        description: Long description of the Location.
        first_issue: First issue the Location appeared in.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Location.
        issue_count: Number of issues the Location appears in.
        name: Name/Title of the Location.
        site_url: Url to the resource in Comicvine.
        start_year: The year the Location was first used.
        summary: Short description of the Location.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = Field(alias="first_appeared_in_issue", default=None)
    id: int  # noqa: A003
    image: Image
    issue_count: Optional[int] = Field(alias="count_of_issue_appearances", default=None)
    name: str
    site_url: str = Field(alias="site_detail_url")
    start_year: Optional[int] = None
    summary: Optional[str] = Field(alias="deck", default=None)


class Location(BaseLocation):
    r"""Extends BaseLocation by including all the list references of a location.

    Attributes:
        issues: List of issues the Location appears in.
        story_arcs: List of story arcs the Location appears in.
        volumes: List of volumes the Location appears in.
    """

    issues: List[IssueEntry] = Field(alias="issue_credits", default_factory=list)
    story_arcs: List[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    volumes: List[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class LocationEntry(BaseLocation):
    """Contains all the fields available when viewing a list of Locations."""
