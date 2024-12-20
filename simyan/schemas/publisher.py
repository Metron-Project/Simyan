"""The Publisher module.

This module provides the following classes:
- BasicPublisher
- Publisher
"""

__all__ = ["BasicPublisher", "Publisher"]

from datetime import datetime
from typing import Optional

from pydantic import Field, HttpUrl

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, Images


class BasicPublisher(BaseModel):
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

    aliases: Optional[str] = None
    api_url: HttpUrl = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    id: int
    image: Images
    location_address: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    name: str
    site_url: HttpUrl = Field(alias="site_detail_url")
    summary: Optional[str] = Field(alias="deck", default=None)


class Publisher(BasicPublisher):
    r"""Extends BasicPublisher by including all the list references of a publisher.

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
