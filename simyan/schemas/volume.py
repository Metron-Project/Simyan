"""
The Volume module.

This module provides the following classes:

- Volume
"""
__all__ = ["Volume"]
import re
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import CountEntry, GenericEntry, ImageEntry, IssueEntry


class Volume(BaseModel):
    r"""
    The Volume object contains information for a volume.

    Attributes:
        aliases: List of names used by the Volume, separated by `~\\r\\n`.
        api_url: Url to the resource in the Comicvine API.
        characters: List of characters in the Volume.
        concepts: List of concepts in the Volume.
        creators: List of creators in the Volume.
        date_added: Date and time when the Volume was added.
        date_last_updated: Date and time when the Volume was last updated.
        description: Long description of the Volume.
        first_issue: First issue of the Volume.
        id_: Identifier used by Comicvine. **Deprecated:** Use volume_id instead.
        volume_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Volume.
        issue_count: Number of issues in the Volume.
        issues: List of issues in the Volume.
        last_issue: Last issue of the Volume.
        locations: List of locations in the Volume.
        name: Name/Title of the Volume.
        objects: List of objects in the Volume.
        publisher: The publisher of the Volume.
        site_url: Url to the resource in Comicvine.
        start_year: The year the Volume started.
        summary: Short description of the Volume.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    characters: List[CountEntry] = Field(default_factory=list)
    concepts: List[CountEntry] = Field(default_factory=list)
    creators: List[CountEntry] = Field(default_factory=list, alias="people")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = None
    id_: int = Field(alias="id")
    volume_id: int = Field(alias="id")
    image: ImageEntry
    issue_count: int = Field(alias="count_of_issues")
    issues: List[IssueEntry] = Field(default_factory=list)
    last_issue: Optional[IssueEntry] = None
    locations: List[CountEntry] = Field(default_factory=list)
    name: str
    objects: List[CountEntry] = Field(default_factory=list)
    publisher: Optional[GenericEntry] = None
    site_url: str = Field(alias="site_detail_url")
    start_year: Optional[int] = None
    summary: Optional[str] = Field(default=None, alias="deck")

    def __init__(self, **data):
        try:
            data["start_year"] = int(data["start_year"] or "")
        except ValueError:
            data["start_year"] = None
        super().__init__(**data)

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Volume has used.

        Returns:
            List of aliases, split by `~\\r\\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []
