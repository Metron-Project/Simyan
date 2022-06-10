"""
The Volume module.

This module provides the following classes:

- Volume
- VolumeResult
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from simyan.schemas.generic_entries import CountEntry, GenericEntry, ImageEntry, IssueEntry


class Volume(BaseModel):
    """The Volume object contains information for a volume."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    date_added: datetime  #: Date and time when the Volume was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Volume was updated on Comicvine.
    id_: int = Field(
        alias="id"
    )  #: Identifier used in Comicvine *Deprecated use volume_id instead*.
    volume_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Volume.
    issue_count: int = Field(alias="count_of_issues")  #: Number of issues in the Volume.
    name: str  #: Name/Title of the Volume.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    aliases: Optional[str] = None  #: List of names the Volume has used, separated by ``\n``.
    description: Optional[str] = None  #: Long description of the Volume.
    first_issue: Optional[IssueEntry] = None  #: First issue of the Volume.
    last_issue: Optional[IssueEntry] = None  #: Last issue of the Volume.
    publisher: Optional[GenericEntry] = None  #: The publisher of the Volume.
    start_year: Optional[int] = None  #: The year the Volume started.
    summary: Optional[str] = Field(default=None, alias="deck")  #: Short description of the Volume.
    characters: List[CountEntry] = Field(default_factory=list)  #: List of characters in the Volume.
    concepts: List[CountEntry] = Field(default_factory=list)  #: List of concepts in the Volume.
    creators: List[CountEntry] = Field(
        default_factory=list, alias="people"
    )  #: List of creators in the Volume.
    issues: List[IssueEntry] = Field(default_factory=list)  #: List of issues in the Volume.
    locations: List[CountEntry] = Field(default_factory=list)  #: List of locations in the Volume.
    objects: List[CountEntry] = Field(default_factory=list)  #: List of objects in the Volume.

    def __init__(self, **data):
        try:
            data["start_year"] = int(data["start_year"] or "")
        except ValueError:
            data["start_year"] = None
        super().__init__(**data)


class VolumeResult(BaseModel):
    """The VolumeResult object contains information for a volume."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    date_added: datetime  #: Date and time when the Volume was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Volume was updated on Comicvine.
    id_: int = Field(
        alias="id"
    )  #: Identifier used in Comicvine *Deprecated use volume_id instead*.
    volume_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Volume.
    issue_count: int = Field(alias="count_of_issues")  #: Number of issues in the Volume.
    name: str  #: Name/Title of the Volume.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    aliases: Optional[str] = None  #: List of names the Volume has used, separated by ``\n``.
    description: Optional[str] = None  #: Long description of the Volume.
    first_issue: Optional[IssueEntry] = None  #: First issue of the Volume.
    last_issue: Optional[IssueEntry] = None  #: Last issue of the Volume.
    publisher: Optional[GenericEntry] = None  #: The publisher of the Volume.
    start_year: Optional[int] = None  #: The year the Volume started.
    summary: Optional[str] = Field(default=None, alias="deck")  #: Short description of the Volume.

    def __init__(self, **data):
        try:
            data["start_year"] = int(data["start_year"] or "")
        except ValueError:
            data["start_year"] = None
        super().__init__(**data)
