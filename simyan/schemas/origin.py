"""The Origin module.

This module provides the following classes:
- BasicOrigin
- Origin
"""

__all__ = ["BasicOrigin", "Origin"]

from typing import Optional

from pydantic import Field, HttpUrl

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry


class BasicOrigin(BaseModel):
    r"""Contains fields for all Origins.

    Attributes:
        api_url: Url to the resource in the Comicvine API.
        id: Identifier used by Comicvine.
        name: Name/Title of the Origin.
        site_url: Url to the resource in Comicvine.
    """

    api_url: HttpUrl = Field(alias="api_detail_url")
    id: int
    name: str
    site_url: HttpUrl = Field(alias="site_detail_url")


class Origin(BasicOrigin):
    r"""Extends BasicOrigin by including all the list references of a origin.

    Attributes:
        character_set:
        characters: List of characters with the Origin.
        profiles:
    """

    character_set: Optional[int] = None
    characters: list[GenericEntry] = Field(default_factory=list)
    profiles: list[int] = Field(default_factory=list)
