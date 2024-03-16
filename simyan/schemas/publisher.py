"""The Publisher module.

This module provides the following classes:

- Publisher
- PublisherEntry
"""

from __future__ import annotations

__all__ = ["Publisher", "PublisherEntry"]
from datetime import datetime

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, Image


class BasePublisher(BaseModel):
    r"""Contains fields for all Publishers.

    Attributes:
        aliases: List of names used by the Publisher, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Publisher was added.
        date_last_updated: Date and time when the Publisher was last updated.
        description: Long description of the Publisher.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Publisher.
        location_address: Address the Publisher is located.
        location_city: City the Publisher is located.
        location_state: State the Publisher is located.
        name: Name/Title of the Publisher.
        site_url: Url to the resource in Comicvine.
        summary: Short description of the Publisher.
    """

    aliases: str | None = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: str | None = None
    id: int
    image: Image
    location_address: str | None = None
    location_city: str | None = None
    location_state: str | None = None
    name: str
    site_url: str = Field(alias="site_detail_url")
    summary: str | None = Field(default=None, alias="deck")


class Publisher(BasePublisher):
    r"""Extends BasePublisher by including all the list references of a publisher.

    Attributes:
        characters: List of characters the Publisher created.
        story_arcs: List of story arcs the Publisher created.
        teams: List of teams the Publisher created.
        volumes: List of volumes the Publisher created.
    """

    characters: list[GenericEntry] = Field(default_factory=list)
    story_arcs: list[GenericEntry] = Field(default_factory=list)
    teams: list[GenericEntry] = Field(default_factory=list)
    volumes: list[GenericEntry] = Field(default_factory=list)


class PublisherEntry(BasePublisher):
    """Contains all the fields available when viewing a list of Publishers."""
