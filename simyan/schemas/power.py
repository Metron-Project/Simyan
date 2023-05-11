"""
The Power module.

This module provides the following classes:

- Power
- PowerEntry
"""
__all__ = ["Power", "PowerEntry"]
import re
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry


class BasePower(BaseModel):
    r"""
    Contains fields for all Powers.

    Attributes:
        aliases: List of names used by the Power, separated by `~\r\n`.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Power was added.
        date_last_updated: Date and time when the Power was last updated.
        description: Long description of the Power.
        name: Name/Title of the Power.
        power_id: Identifier used by Comicvine.
        site_url: Url to the resource in Comicvine.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    name: str
    power_id: int = Field(alias="id")
    site_url: str = Field(alias="site_detail_url")

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Power has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []


class Power(BasePower):
    r"""
    Extends BasePower by including all the list references of a power.

    Attributes:
        characters: List of characters with the Power.
    """

    characters: List[GenericEntry] = Field(default_factory=list)


class PowerEntry(BasePower):
    """Contains all the fields available when viewing a list of Powers."""
