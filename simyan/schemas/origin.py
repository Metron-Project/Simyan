"""The Origin module.

This module provides the following classes:

- Origin
- OriginEntry
"""
__all__ = ["Origin", "OriginEntry"]
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry


class BaseOrigin(BaseModel):
    r"""Contains fields for all Origins.

    Attributes:
        api_url: Url to the resource in the Comicvine API.
        id: Identifier used by Comicvine.
        name: Name/Title of the Origin.
        site_url: Url to the resource in Comicvine.
    """

    api_url: str = Field(alias="api_detail_url")
    id: int  # noqa: A003
    name: str
    site_url: str = Field(alias="site_detail_url")


class Origin(BaseOrigin):
    r"""Extends BaseOrigin by including all the list references of a origin.

    Attributes:
        character_set: Unknown field
        characters: List of characters with the Origin.
        profiles: Unknown field
    """

    character_set: Optional[int] = None
    characters: List[GenericEntry] = Field(default_factory=list)
    profiles: List[int] = Field(default_factory=list)


class OriginEntry(BaseOrigin):
    """Contains all the fields available when viewing a list of Origins."""
