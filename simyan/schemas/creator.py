"""
The Creator module.

This module provides the following classes:

- Creator
"""
import re
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from simyan.schemas.generic_entries import GenericEntry, ImageEntry


class Creator(BaseModel):
    """The Creator object contains information for a creator."""

    aliases: Optional[str] = Field(
        default=None
    )  #: List of names the Creator has used, separated by ``\n``.
    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    characters: List[GenericEntry] = Field(
        default_factory=list, alias="created_characters"
    )  #: List of characters the Creator has created.
    country: Optional[str] = Field(default=None)  #: Country where the Creator is from.
    date_added: datetime  #: Date and time when the Creator was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Creator was updated on Comicvine.
    date_of_birth: Optional[date] = Field(
        default=None, alias="birth"
    )  #: Date when the Creator was born.
    date_of_death: Optional[date] = Field(
        default=None, alias="death"
    )  #: Date when the Creator died.
    description: Optional[str] = Field(default=None)  #: Long description of the Creator.
    email: Optional[str] = Field(default=None)  #: Email address of the Creator.
    gender: int  #: Creator gender.
    hometown: Optional[str] = Field(default=None)  #: Hometown of the Creator.
    id_: int = Field(alias="id")  #: Identifier used in Comicvine.
    creator_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Creator.
    issue_count: Optional[int] = Field(
        default=None, alias="count_of_isssue_appearances"
    )  #: Number of issues the Creator appears in.
    issues: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of issues the Creator appears in.
    name: str  #: Name of the Creator.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    story_arcs: List[GenericEntry] = Field(
        default_factory=list, alias="story_arc_credits"
    )  #: List of story arcs the Creator appears in.
    summary: Optional[str] = Field(default=None, alias="deck")  #: Short description of the Creator.
    volumes: List[GenericEntry] = Field(
        default_factory=list, alias="volume_credits"
    )  #: List of volumes the Creator appears in.
    website: Optional[str] = Field(default=None)  #: Url to the Creator's website.

    def __init__(self, **data):
        if "death" in data and data["death"] is not None:
            data["death"] = data["death"]["date"].split()[0]
        if data["birth"]:
            data["birth"] = data["birth"].split()[0]
        super().__init__(**data)

    @property
    def alias_list(self) -> List[str]:
        """List of names the Creator has used."""
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.ignore
