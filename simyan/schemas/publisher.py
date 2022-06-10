"""
The Publisher module.

This module provides the following classes:

- Publisher
- PublisherResult
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from simyan.schemas.generic_entries import GenericEntry, ImageEntry


class Publisher(BaseModel):
    """The Publisher object contains information for a publisher."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    date_added: datetime  #: Date and time when the Publisher was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Publisher was updated on Comicvine.
    id_: int = Field(
        alias="id"
    )  #: Identifier used in Comicvine *Deprecated use publisher_id instead*.
    publisher_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Publisher.
    name: str  #: Name/Title of the Publisher.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    aliases: Optional[str] = None  #: List of names the Publisher has used, separated by ``\n``.
    description: Optional[str] = None  #: Long description of the Publisher.
    location_address: Optional[str] = None  #: Address of the Publisher.
    location_city: Optional[str] = None  #: City where the Publisher is.
    location_state: Optional[str] = None  #: State where the Publisher is.
    summary: Optional[str] = Field(
        default=None, alias="deck"
    )  #: Short description of the Publisher.
    characters: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of characters the Publisher created.
    story_arcs: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of story arcs the Publisher created.
    teams: List[GenericEntry] = Field(default_factory=list)  #: List of teams the Publisher created.
    volumes: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of volumes the Publisher created.


class PublisherResult(BaseModel):
    """The PublisherResult object contains information for a publisher."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    date_added: datetime  #: Date and time when the Publisher was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Publisher was updated on Comicvine.
    id_: int = Field(
        alias="id"
    )  #: Identifier used in Comicvine *Deprecated use publisher_id instead*.
    publisher_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Publisher.
    name: str  #: Name/Title of the Publisher.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    aliases: Optional[str] = None  #: List of names the Publisher has used, separated by ``\n``.
    description: Optional[str] = None  #: Long description of the Publisher.
    location_address: Optional[str] = None  #: Address of the Publisher.
    location_city: Optional[str] = None  #: City where the Publisher is.
    location_state: Optional[str] = None  #: State where the Publisher is.
    summary: Optional[str] = Field(
        default=None, alias="deck"
    )  #: Short description of the Publisher.
