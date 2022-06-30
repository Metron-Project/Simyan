"""
The Publisher module.

This module provides the following classes:

- Publisher
"""
import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from simyan.schemas.generic_entries import GenericEntry, ImageEntry


class Publisher(BaseModel):
    """The Publisher object contains information for a publisher."""

    aliases: Optional[str] = Field(
        default=None
    )  #: List of names the Publisher has used, separated by ``\n``.
    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    characters: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of characters the Publisher created.
    date_added: datetime  #: Date and time when the Publisher was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Publisher was updated on Comicvine.
    description: Optional[str] = Field(default=None)  #: Long description of the Publisher.
    id_: int = Field(alias="id")  #: Identifier used in Comicvine.
    publisher_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Publisher.
    location_address: Optional[str] = Field(default=None)  #: Address of the Publisher.
    location_city: Optional[str] = Field(default=None)  #: City where the Publisher is.
    location_state: Optional[str] = Field(default=None)  #: State where the Publisher is.
    name: str  #: Name/Title of the Publisher.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    story_arcs: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of story arcs the Publisher created.
    summary: Optional[str] = Field(
        default=None, alias="deck"
    )  #: Short description of the Publisher.
    teams: List[GenericEntry] = Field(default_factory=list)  #: List of teams the Publisher created.
    volumes: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of volumes the Publisher created.

    @property
    def alias_list(self) -> List[str]:
        """List of names the Publisher has used."""
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.ignore
