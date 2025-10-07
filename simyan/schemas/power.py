"""The Power module.

This module provides the following classes:
- BasicPower
- Power
"""

__all__ = ["BasicPower", "Power"]

from datetime import datetime

from pydantic import Field, HttpUrl

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry


class BasicPower(BaseModel):
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

    aliases: str | None = None
    api_url: HttpUrl = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: str | None = None
    id: int
    name: str
    site_url: HttpUrl = Field(alias="site_detail_url")


class Power(BasicPower):
    r"""Extends BasicPower by including all the list references of a power.

    Attributes:
        characters: List of characters with the Power.
    """

    characters: list[GenericEntry] = Field(default_factory=list)
