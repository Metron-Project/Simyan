"""
The Publisher module.

This module provides the following classes:

- Publisher
"""
__all__ = ["Publisher"]
import re
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, ImageEntry


class Publisher(BaseModel):
    r"""
    The Publisher object contains information for a publisher.

    Attributes:
        aliases: List of names used by the Publisher, separated by `~\\r\\n`.
        api_url: Url to the resource in the Comicvine API.
        characters: List of characters the Publisher created.
        date_added: Date and time when the Publisher was added.
        date_last_updated: Date and time when the Publisher was last updated.
        description: Long description of the Publisher.
        id_: Identifier used by Comicvine. **Deprecated:** Use publisher_id instead.
        publisher_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Publisher.
        location_address: Address where the Publisher is located.
        location_city: City where the Publisher is located.
        location_state: State where the Publisher is located.
        name: Name/Title of the Publisher.
        site_url: Url to the resource in Comicvine.
        story_arcs: List of story arcs the Publisher created.
        summary: Short description of the Publisher.
        teams: List of teams the Publisher created.
        volumes: List of volumes the Publisher created.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    characters: List[GenericEntry] = Field(default_factory=list)
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    id_: int = Field(alias="id")
    publisher_id: int = Field(alias="id")
    image: ImageEntry
    location_address: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    name: str
    site_url: str = Field(alias="site_detail_url")
    story_arcs: List[GenericEntry] = Field(default_factory=list)
    summary: Optional[str] = Field(default=None, alias="deck")
    teams: List[GenericEntry] = Field(default_factory=list)
    volumes: List[GenericEntry] = Field(default_factory=list)

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Publisher has used.

        Returns:
            List of aliases, split by `~\\r\\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []
