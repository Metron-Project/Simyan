"""
The Creator module.

This module provides the following classes:

- Creator
- CreatorResult
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from dataclasses_json import Undefined, config, dataclass_json
from marshmallow import fields

from simyan.schemas.generic_entries import GenericEntry, ImageEntry


def pre_process_creator(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Only keep the date of death and date of birth information from ComicVine. \
    The timezone info they include is not of any use.

    Args:
        entry: Data from the Comicvine response.

    Returns:
        Comicvine response with the date of death and date of birth information included.
    """
    if "death" in entry and entry["death"] is not None:
        entry["death"] = entry["death"]["date"].split()[0]
    if entry["birth"]:
        entry["birth"] = entry["birth"].split()[0]
    return entry


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Creator:
    """The Creator object contains information for a creator."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    country: str  #: Country where the Creator is from.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Creator was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Creator was updated on Comicvine.
    description: str  #: Long description of the Creator.
    gender: int  #: Creator gender.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Creator.
    name: str  #: Name of the Creator.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Creator has used, separated by ``\n``.
    characters: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="created_characters")
    )  #: List of characters the Creator has created.
    date_of_birth: Optional[date] = field(
        default=None,
        metadata=config(
            field_name="birth",
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
        ),
    )  #: Date when the Creator was born.
    date_of_death: Optional[date] = field(
        default=None,
        metadata=config(
            field_name="death",
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
        ),
    )  #: Date when the Creator died.
    email: Optional[str] = field(default=None)  #: Email address of the Creator.
    hometown: Optional[str] = field(default=None)  #: Hometown of the Creator.
    issue_count: Optional[int] = field(
        default=None, metadata=config(field_name="count_of_isssue_appearances")
    )  #: Number of issues the Creator appears in.
    issues: List[GenericEntry] = field(
        default_factory=list
    )  #: List of issues the Creator appears in.
    story_arcs: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="story_arc_credits")
    )  #: List of story arcs the Creator appears in.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Creator.
    volumes: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="volume_credits")
    )  #: List of volumes the Creator appears in.
    website: Optional[str] = field(default=None)  #: Url to the Creator's website.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CreatorResult:
    """The CreatorResult object contains information for a creator."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    country: str  #: Country where the Creator is from.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Creator was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Creator was updated on Comicvine.
    description: str  #: Long description of the Creator.
    gender: int  #: Creator gender.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Creator.
    name: str  #: Name of the Creator.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Creator has used, separated by ``\n``.
    date_of_birth: Optional[date] = field(
        default=None,
        metadata=config(
            field_name="birth",
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
        ),
    )  #: Date when the Creator was born.
    date_of_death: Optional[date] = field(
        default=None,
        metadata=config(
            field_name="death",
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
        ),
    )  #: Date when the Creator died.
    email: Optional[str] = field(default=None)  #: Email address of the Creator.
    hometown: Optional[str] = field(default=None)  #: Hometown of the Creator.
    issue_count: Optional[int] = field(
        default=None, metadata=config(field_name="count_of_isssue_appearances")
    )  #: Number of issues the Creator appears in.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Creator.
    website: Optional[str] = field(default=None)  #: Url to the Creator's website.
