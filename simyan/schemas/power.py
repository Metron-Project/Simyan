"""The Power module.

This module provides the following classes:

- Power
- PowerEntry
"""
__all__ = ["Power", "PowerEntry"]
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry


class BasePower(BaseModel):
    r"""Contains fields for all Powers.

    Attributes:
        aliases: List of names used by the Power, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Power was added.
        date_last_updated: Date and time when the Power was last updated.
        description: Long description of the Power.
        id: Identifier used by Comicvine.
        name: Name/Title of the Power.
        site_url: Url to the resource in Comicvine.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    id: int  # noqa: A003
    name: str
    site_url: str = Field(alias="site_detail_url")


class Power(BasePower):
    r"""Extends BasePower by including all the list references of a power.

    Attributes:
        characters: List of characters with the Power.
    """

    characters: List[GenericEntry] = Field(default_factory=list)


class PowerEntry(BasePower):
    """Contains all the fields available when viewing a list of Powers."""
