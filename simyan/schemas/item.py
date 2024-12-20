"""The Item module.

This module provides the following classes:
- BasicItem
- Item
"""

__all__ = ["BasicItem", "Item"]

from datetime import datetime
from typing import Optional

from pydantic import Field, HttpUrl

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, GenericIssue, Images


class BasicItem(BaseModel):
    r"""Contains fields for all Items.

    Attributes:
        aliases: List of names used by the Item, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Item was added.
        date_last_updated: Date and time when the Item was last updated.
        description: Long description of the Item.
        first_issue: First issue the Item appeared in.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Item.
        issue_count: Number of issues the Item appears in.
        name: Name/Title of the Item.
        site_url: Url to the resource in Comicvine.
        start_year: The year the Item first appeared.
        summary: Short description of the Item.
    """

    aliases: Optional[str] = None
    api_url: HttpUrl = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[GenericIssue] = Field(alias="first_appeared_in_issue", default=None)
    id: int
    image: Images
    issue_count: int = Field(alias="count_of_issue_appearances")
    name: str
    site_url: HttpUrl = Field(alias="site_detail_url")
    start_year: Optional[int] = None
    summary: Optional[str] = Field(alias="deck", default=None)


class Item(BasicItem):
    r"""Extends BasicItem by including all the list references of a item.

    Attributes:
        issues: List of issues the Item appears in.
        story_arcs: List of story arcs the Item appears in.
        volumes: List of volumes the Item appears in.
    """

    issues: list[GenericEntry] = Field(alias="issue_credits", default_factory=list)
    story_arcs: list[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    volumes: list[GenericEntry] = Field(alias="volume_credits", default_factory=list)
