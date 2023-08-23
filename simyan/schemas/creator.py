"""The Creator module.

This module provides the following classes:

- Creator
- CreatorEntry
"""
__all__ = ["Creator", "CreatorEntry"]
from datetime import date, datetime
from typing import Any, List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, Image


class BaseCreator(BaseModel):
    r"""Contains fields for all Creators.

    Attributes:
        aliases: List of names used by the Creator, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        country: Country of origin.
        date_added: Date and time when the Creator was added.
        date_last_updated: Date and time when the Creator was last updated.
        date_of_birth: Date when the Creator was born.
        date_of_death: Date when the Creator died.
        description: Long description of the Creator.
        email: Email address of the Creator.
        gender: Creator gender.
        hometown: Hometown of the Creator.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Creator.
        issue_count: Number of issues the Creator appears in.
        name: Name/Title of the Creator.
        site_url: Url to the resource in Comicvine.
        summary: Short description of the Creator.
        website: Url to the Creator's website.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    country: Optional[str] = None
    date_added: datetime
    date_last_updated: datetime
    date_of_birth: Optional[date] = Field(alias="birth", default=None)
    date_of_death: Optional[date] = Field(alias="death", default=None)
    description: Optional[str] = None
    email: Optional[str] = None
    gender: int
    hometown: Optional[str] = None
    id: int  # noqa: A003
    image: Image
    issue_count: Optional[int] = Field(alias="count_of_isssue_appearances", default=None)
    name: str
    site_url: str = Field(alias="site_detail_url")
    summary: Optional[str] = Field(alias="deck", default=None)
    website: Optional[str] = None

    def __init__(self: "BaseCreator", **data: Any):
        if "death" in data and data["death"]:
            data["death"] = data["death"]["date"].split()[0]
        if "birth" in data and data["birth"]:
            data["birth"] = data["birth"].split()[0]
        super().__init__(**data)


class Creator(BaseCreator):
    r"""Extends BaseCreator by including all the list references of a creator.

    Attributes:
        characters: List of characters the Creator has created.
        issues: List of issues the Creator appears in.
        story_arcs: List of story arcs the Creator appears in.
        volumes: List of volumes the Creator appears in.
    """

    characters: List[GenericEntry] = Field(alias="created_characters", default_factory=list)
    issues: List[GenericEntry] = Field(default_factory=list)
    story_arcs: List[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    volumes: List[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class CreatorEntry(BaseCreator):
    """Contains all the fields available when viewing a list of Creators."""
