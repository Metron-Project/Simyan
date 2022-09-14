"""
The Creator module.

This module provides the following classes:

- Creator
- CreatorEntry
"""
__all__ = ["Creator", "CreatorEntry"]
import re
from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, ImageEntry


class Creator(BaseModel):
    r"""
    The Creator object contains information for a creator.

    Attributes:
        aliases: List of names used by the Creator, separated by `~\r\n`
        api_url: Url to the resource in the Comicvine API.
        characters: List of characters the Creator has created.
        country: Country of origin.
        date_added: Date and time when the Creator was added.
        date_last_updated: Date and time when the Creator was last updated.
        date_of_birth: Date when the Creator was born.
        date_of_death: Date when the Creator died.
        description: Long description of the Creator.
        email: Email address of the Creator.
        gender: Creator gender.
        hometown: Hometown of the Creator.
        creator_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Creator.
        issue_count: Number of issues the Creator appears in.
        issues: List of issues the Creator appears in.
        name: Name/Title of the Creator.
        site_url: Url to the resource in Comicvine.
        story_arcs: List of story arcs the Creator appears in.
        summary: Short description of the Creator.
        volumes: List of volumes the Creator appears in.
        website: Url to the Creator's website.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    characters: List[GenericEntry] = Field(default_factory=list, alias="created_characters")
    country: Optional[str] = None
    date_added: datetime
    date_last_updated: datetime
    date_of_birth: Optional[date] = Field(default=None, alias="birth")
    date_of_death: Optional[date] = Field(default=None, alias="death")
    description: Optional[str] = None
    email: Optional[str] = None
    gender: int
    hometown: Optional[str] = None
    creator_id: int = Field(alias="id")
    image: ImageEntry
    issue_count: Optional[int] = Field(default=None, alias="count_of_isssue_appearances")
    issues: List[GenericEntry] = Field(default_factory=list)
    name: str
    site_url: str = Field(alias="site_detail_url")
    story_arcs: List[GenericEntry] = Field(default_factory=list, alias="story_arc_credits")
    summary: Optional[str] = Field(default=None, alias="deck")
    volumes: List[GenericEntry] = Field(default_factory=list, alias="volume_credits")
    website: Optional[str] = None

    def __init__(self, **data):
        if "death" in data and data["death"] is not None:
            data["death"] = data["death"]["date"].split()[0]
        if data["birth"]:
            data["birth"] = data["birth"].split()[0]
        super().__init__(**data)

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Creator has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []


class CreatorEntry(BaseModel):
    r"""
    The CreatorEntry object contains information for a creator.

    Attributes:
        aliases: List of names used by the CreatorEntry, separated by `~\r\n`
        api_url: Url to the resource in the Comicvine API.
        country: Country of origin.
        date_added: Date and time when the CreatorEntry was added.
        date_last_updated: Date and time when the CreatorEntry was last updated.
        date_of_birth: Date when the CreatorEntry was born.
        date_of_death: Date when the CreatorEntry died.
        description: Long description of the CreatorEntry.
        email: Email address of the CreatorEntry.
        gender: CreatorEntry gender.
        hometown: Hometown of the CreatorEntry.
        creator_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the CreatorEntry.
        issue_count: Number of issues the CreatorEntry appears in.
        name: Name/Title of the CreatorEntry.
        site_url: Url to the resource in Comicvine.
        summary: Short description of the CreatorEntry.
        website: Url to the CreatorEntry's website.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    country: Optional[str] = None
    date_added: datetime
    date_last_updated: datetime
    date_of_birth: Optional[date] = Field(default=None, alias="birth")
    date_of_death: Optional[date] = Field(default=None, alias="death")
    description: Optional[str] = None
    email: Optional[str] = None
    gender: int
    hometown: Optional[str] = None
    creator_id: int = Field(alias="id")
    image: ImageEntry
    issue_count: Optional[int] = Field(default=None, alias="count_of_isssue_appearances")
    name: str
    site_url: str = Field(alias="site_detail_url")
    summary: Optional[str] = Field(default=None, alias="deck")
    website: Optional[str] = None

    def __init__(self, **data):
        if "death" in data and data["death"] is not None:
            data["death"] = data["death"]["date"].split()[0]
        if data["birth"]:
            data["birth"] = data["birth"].split()[0]
        super().__init__(**data)

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the CreatorEntry has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []
