"""
The StoryArc module.

This module provides the following classes:

- StoryArc
- StoryArcResult
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from dataclasses_json import Undefined, config, dataclass_json
from marshmallow import fields

from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class StoryArc:
    """The StoryArc object contains information for a story arc."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Story Arc was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Story Arc was updated on Comicvine.
    first_issue: IssueEntry = field(
        metadata=config(field_name="first_appeared_in_issue")
    )  #: First issue of the Story Arc.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Story Arc.
    issue_count: int = field(
        metadata=config(field_name="count_of_isssue_appearances")
    )  #: Number of issues in the Story Arc.
    name: str  #: Name/Title of the Story Arc.
    publisher: GenericEntry  #: The publisher of the Story Arc.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Story Arc has used, separated by ``\n``.
    description: Optional[str] = field(default=None)  #: Long description of the Story Arc.
    issues: List[GenericEntry] = field(default_factory=list)  #: List of issues in the Story Arc.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Story Arc.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class StoryArcResult:
    """The StoryArcResult object contains information for a story arc."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Story Arc was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Story Arc was updated on Comicvine.
    first_issue: IssueEntry = field(
        metadata=config(field_name="first_appeared_in_issue")
    )  #: First issue of the Story Arc.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Story Arc.
    issue_count: int = field(
        metadata=config(field_name="count_of_isssue_appearances")
    )  #: Number of issues in the Story Arc.
    name: str  #: Name/Title of the Story Arc.
    publisher: GenericEntry  #: The publisher of the Story Arc.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Story Arc has used, separated by ``\n``.
    description: Optional[str] = field(default=None)  #: Long description of the Story Arc.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Story Arc.
