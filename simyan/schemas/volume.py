"""
The Volume module.

This module provides the following classes:

- Volume
"""
import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from simyan.schemas.generic_entries import CountEntry, GenericEntry, ImageEntry, IssueEntry


class Volume(BaseModel):
    """The Volume object contains information for a volume."""

    aliases: Optional[str] = Field(
        default=None
    )  #: List of names the Volume has used, separated by ``\n``.
    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    characters: List[CountEntry] = Field(default_factory=list)  #: List of characters in the Volume.
    concepts: List[CountEntry] = Field(default_factory=list)  #: List of concepts in the Volume.
    creators: List[CountEntry] = Field(
        default_factory=list, alias="people"
    )  #: List of creators in the Volume.
    date_added: datetime  #: Date and time when the Volume was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Volume was updated on Comicvine.
    description: Optional[str] = Field(default=None)  #: Long description of the Volume.
    first_issue: Optional[IssueEntry] = Field(default=None)  #: First issue of the Volume.
    id_: int = Field(alias="id")  #: Identifier used in Comicvine.
    volume_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Volume.
    issue_count: int = Field(alias="count_of_issues")  #: Number of issues in the Volume.
    issues: List[IssueEntry] = Field(default_factory=list)  #: List of issues in the Volume.
    last_issue: Optional[IssueEntry] = Field(default=None)  #: Last issue of the Volume.
    locations: List[CountEntry] = Field(default_factory=list)  #: List of locations in the Volume.
    name: str  #: Name/Title of the Volume.
    objects: List[CountEntry] = Field(default_factory=list)  #: List of objects in the Volume.
    publisher: Optional[GenericEntry] = Field(default=None)  #: The publisher of the Volume.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    start_year: Optional[int] = Field(default=None)  #: The year the Volume started.
    summary: Optional[str] = Field(default=None, alias="deck")  #: Short description of the Volume.

    def __init__(self, **data):
        try:
            data["start_year"] = int(data["start_year"] or "")
        except ValueError:
            data["start_year"] = None
        super().__init__(**data)

    @property
    def alias_list(self) -> List[str]:
        """List of names the Volume has used."""
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.ignore
