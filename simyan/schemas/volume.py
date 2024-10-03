"""The Volume module.

This module provides the following classes:

- Volume
- VolumeEntry
"""

from __future__ import annotations

__all__ = ["Volume", "VolumeEntry"]
from datetime import datetime

from pydantic import Field, field_validator

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import CountEntry, GenericEntry, Image, IssueEntry


class BaseVolume(BaseModel):
    r"""Contains fields for all Volumes.

    Attributes:
        aliases: List of names used by the Volume, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Volume was added.
        date_last_updated: Date and time when the Volume was last updated.
        description: Long description of the Volume.
        first_issue: First issue of the Volume.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Volume.
        issue_count: Number of issues in the Volume.
        last_issue: Last issue of the Volume.
        name: Name/Title of the Volume.
        publisher: The publisher of the Volume.
        site_url: Url to the resource in Comicvine.
        start_year: The year the Volume started.
        summary: Short description of the Volume.
    """

    aliases: str | None = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: str | None = None
    first_issue: IssueEntry | None = None
    id: int
    image: Image
    issue_count: int = Field(alias="count_of_issues")
    last_issue: IssueEntry | None = None
    name: str
    publisher: GenericEntry | None = None
    site_url: str = Field(alias="site_detail_url")
    start_year: int | None = None
    summary: str | None = Field(alias="deck", default=None)

    @field_validator("start_year", mode="before")
    def validate_start_year(cls, v: str) -> int | None:
        """Convert start_year to int or None.

        Args:
            v: String value of the start_year

        Returns:
            int or None version of the start_year
        """
        if v:
            try:
                return int(v)
            except ValueError:
                return None
        return None


class Volume(BaseVolume):
    r"""Extends BaseVolume by including all the list references of a volume.

    Attributes:
        characters: List of characters in the Volume.
        concepts: List of concepts in the Volume.
        creators: List of creators in the Volume.
        issues: List of issues in the Volume.
        locations: List of locations in the Volume.
        objects: List of objects in the Volume.
    """

    characters: list[CountEntry] = Field(default_factory=list)
    concepts: list[CountEntry] = Field(default_factory=list)
    creators: list[CountEntry] = Field(alias="people", default_factory=list)
    issues: list[IssueEntry] = Field(default_factory=list)
    locations: list[CountEntry] = Field(default_factory=list)
    objects: list[CountEntry] = Field(default_factory=list)


class VolumeEntry(BaseVolume):
    """Contains all the fields available when viewing a list of Volumes."""
