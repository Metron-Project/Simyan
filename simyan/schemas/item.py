"""The Item module.

This module provides the following classes:

- Item
- ItemEntry
"""

from __future__ import annotations

__all__ = ["Item", "ItemEntry"]
from datetime import datetime

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, Image, IssueEntry


class BaseItem(BaseModel):
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

    aliases: str | None = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: str | None = None
    first_issue: IssueEntry | None = Field(alias="first_appeared_in_issue", default=None)
    id: int
    image: Image
    issue_count: int = Field(alias="count_of_issue_appearances")
    name: str
    site_url: str = Field(alias="site_detail_url")
    start_year: int | None = None
    summary: str | None = Field(alias="deck", default=None)


class Item(BaseItem):
    r"""Extends BaseItem by including all the list references of a item.

    Attributes:
        issues: List of issues the Item appears in.
        story_arcs: List of story arcs the Item appears in.
        volumes: List of volumes the Item appears in.
    """

    issues: list[GenericEntry] = Field(alias="issue_credits", default_factory=list)
    story_arcs: list[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    volumes: list[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class ItemEntry(BaseItem):
    """Contains all the fields available when viewing a list of Items."""
