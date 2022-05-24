"""
The Volume module.

This module provides the following classes:

- Volume
- VolumeResult
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from dataclasses_json import Undefined, config, dataclass_json
from marshmallow import fields

from simyan.schemas.generic_entries import CountEntry, GenericEntry, ImageEntry, IssueEntry


def pre_process_volume(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle non-int values for start_year.

    Args:
        entry: Data from the Comicvine response

    Returns:
        Comicvine response with the start year either None or Int.
    """
    try:
        entry["start_year"] = int(entry["start_year"] or "")
    except ValueError:
        entry["start_year"] = None
    return entry


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Volume:
    """The Volume object contains information for a volume."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Volume was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Volume was updated on Comicvine.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Volume.
    issue_count: int = field(
        metadata=config(field_name="count_of_issues")
    )  #: Number of issues in the Volume.
    name: str  #: Name/Title of the Volume.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Volume has used, separated by ``\n``.
    description: Optional[str] = field(default=None)  #: Long description of the Volume.
    first_issue: Optional[IssueEntry] = field(default=None)  #: First issue of the Volume.
    last_issue: Optional[IssueEntry] = field(default=None)  #: Last issue of the Volume.
    publisher: Optional[GenericEntry] = field(default=None)  #: The publisher of the Volume.
    start_year: Optional[int] = field(default=None)  #: The year the Volume started.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Volume.
    characters: List[CountEntry] = field(default_factory=list)  #: List of characters in the Volume.
    concepts: List[CountEntry] = field(default_factory=list)  #: List of concepts in the Volume.
    creators: List[CountEntry] = field(
        default_factory=list, metadata=config(field_name="people")
    )  #: List of creators in the Volume.
    issues: List[IssueEntry] = field(default_factory=list)  #: List of issues in the Volume.
    locations: List[CountEntry] = field(default_factory=list)  #: List of locations in the Volume.
    objects: List[CountEntry] = field(default_factory=list)  #: List of objects in the Volume.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class VolumeResult:
    """The VolumeResult object contains information for a volume."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Volume was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Volume was updated on Comicvine.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Volume.
    issue_count: int = field(
        metadata=config(field_name="count_of_issues")
    )  #: Number of issues in the Volume.
    name: str  #: Name/Title of the Volume.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Volume has used, separated by ``\n``.
    description: Optional[str] = field(default=None)  #: Long description of the Volume.
    first_issue: Optional[IssueEntry] = field(default=None)  #: First issue of the Volume.
    last_issue: Optional[IssueEntry] = field(default=None)  #: Last issue of the Volume.
    publisher: Optional[GenericEntry] = field(default=None)  #: The publisher of the Volume.
    start_year: Optional[int] = field(default=None)  #: The year the Volume started.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Volume.
