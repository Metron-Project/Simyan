"""
The Publisher module.

This module provides the following classes:

- Publisher
- PublisherResult
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from dataclasses_json import Undefined, config, dataclass_json
from marshmallow import fields

from simyan.schemas.generic_entries import GenericEntry, ImageEntry


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Publisher:
    """The Publisher object contains information for a publisher."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Publisher was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Publisher was updated on Comicvine.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Publisher.
    name: str  #: Name/Title of the Publisher.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Publisher has used, separated by ``\n``.
    description: Optional[str] = field(default=None)  #: Long description of the Publisher.
    location_address: Optional[str] = field(default=None)  #: Address of the Publisher.
    location_city: Optional[str] = field(default=None)  #: City where the Publisher is.
    location_state: Optional[str] = field(default=None)  #: State where the Publisher is.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Publisher.
    characters: List[GenericEntry] = field(
        default_factory=list
    )  #: List of characters the Publisher created.
    story_arcs: List[GenericEntry] = field(
        default_factory=list
    )  #: List of story arcs the Publisher created.
    teams: List[GenericEntry] = field(default_factory=list)  #: List of teams the Publisher created.
    volumes: List[GenericEntry] = field(
        default_factory=list
    )  #: List of volumes the Publisher created.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PublisherResult:
    """The PublisherResult object contains information for a publisher."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Publisher was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Publisher was updated on Comicvine.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Publisher.
    name: str  #: Name/Title of the Publisher.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Publisher has used, separated by ``\n``.
    description: Optional[str] = field(default=None)  #: Long description of the Publisher.
    location_address: Optional[str] = field(default=None)  #: Address of the Publisher.
    location_city: Optional[str] = field(default=None)  #: City where the Publisher is.
    location_state: Optional[str] = field(default=None)  #: State where the Publisher is.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Publisher.
