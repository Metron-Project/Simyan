"""
The GenericEntries module.

This module provides the following classes:

- GenericEntry
- CountEntry
- IssueEntry
- CreatorEntry
- ImageEntry
"""
import re
from typing import List, Optional

from pydantic import BaseModel, Extra, Field


class GenericEntry(BaseModel):
    """The GenericEntry object contains generic information."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the ComicVine API.
    id_: int = Field(alias="id")  #: Identifier used in ComicVine.
    name: Optional[str] = Field(default=None)
    site_url: Optional[str] = Field(
        default=None, alias="site_detail_url"
    )  #: Url to the ComicVine Website.

    class Config:
        """Any extra fields will raise an error, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.forbid


class CountEntry(GenericEntry):
    """The CountEntry object contains generic information with an added count field."""

    count: int

    class Config:
        """Any extra fields will raise an error, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.forbid


class IssueEntry(GenericEntry):
    """The IssueEntry object contains generic information with an added number field."""

    number: Optional[str] = Field(default=None, alias="issue_number")

    class Config:
        """Any extra fields will raise an error, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.forbid


class CreatorEntry(GenericEntry):
    """The CreatorEntry object contains generic information with an added roles field."""

    roles: str = Field(alias="role")  #: separated by ``\n``.

    @property
    def role_list(self) -> List[str]:
        """List of roles the Creator has used."""
        return re.split(r"[~\r\n]+", self.roles) if self.roles else []

    class Config:
        """Any extra fields will raise an error, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.forbid


class ImageEntry(BaseModel):
    """The ImageEntry object contains image information."""

    icon: str = Field(alias="icon_url")  #: Url to image of Icon size.
    medium: str = Field(alias="medium_url")  #: Url to image of Medium size.
    screen: str = Field(alias="screen_url")  #: Url to image of Screen size.
    screen_large: str = Field(alias="screen_large_url")  #: Url to image of Screen Large size.
    small: str = Field(alias="small_url")  #: Url to image of Small size.
    super: str = Field(alias="super_url")  #: Url to image of Super size.
    thumbnail: str = Field(alias="thumb_url")  #: Url to image of Thumbnail size.
    tiny: str = Field(alias="tiny_url")  #: Url to image of Tiny size.
    original: str = Field(alias="original_url")  #: Url to image of Original size.
    tags: Optional[str] = Field(default=None, alias="image_tags")

    class Config:
        """Any extra fields will raise an error, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.forbid
