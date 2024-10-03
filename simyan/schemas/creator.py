"""The Creator module.

This module provides the following classes:

- Creator
- CreatorEntry
"""

from __future__ import annotations

__all__ = ["Creator", "CreatorEntry"]
from datetime import date, datetime
from typing import Any

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

    aliases: str | None = None
    api_url: str = Field(alias="api_detail_url")
    country: str | None = None
    date_added: datetime
    date_last_updated: datetime
    date_of_birth: date | None = Field(alias="birth", default=None)
    date_of_death: date | None = Field(alias="death", default=None)
    description: str | None = None
    email: str | None = None
    gender: int
    hometown: str | None = None
    id: int
    image: Image
    issue_count: int | None = Field(alias="count_of_isssue_appearances", default=None)
    name: str
    site_url: str = Field(alias="site_detail_url")
    summary: str | None = Field(alias="deck", default=None)
    website: str | None = None

    def __init__(self, **data: Any):
        if data.get("death"):
            data["death"] = data["death"]["date"].split()[0]
        if data.get("birth"):
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

    characters: list[GenericEntry] = Field(alias="created_characters", default_factory=list)
    issues: list[GenericEntry] = Field(default_factory=list)
    story_arcs: list[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    volumes: list[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class CreatorEntry(BaseCreator):
    """Contains all the fields available when viewing a list of Creators."""
