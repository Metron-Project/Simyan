"""
The GenericEntries module.

This module provides the following classes:

- GenericEntry
- CountEntry
- IssueEntry
- CreatorEntry
- ImageEntry
"""
__all__ = ["GenericEntry", "CountEntry", "IssueEntry", "CreatorEntry", "ImageEntry"]
import re
from typing import List, Optional

from pydantic import BaseModel, Extra, Field


class GenericEntry(BaseModel):
    """
    The GenericEntry object contains generic information.

    Attributes:
        api_url: Url to the resource in the Comicvine API.
        id_: Identifier used by Comicvine.
        name:
        site_url: Url to the resource in Comicvine.
    """

    api_url: str = Field(alias="api_detail_url")
    id_: int = Field(alias="id")
    name: Optional[str] = Field(default=None)
    site_url: Optional[str] = Field(default=None, alias="site_detail_url")

    class Config:
        """Any extra fields will raise an error."""

        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.forbid


class CountEntry(GenericEntry):
    """
    The CountEntry object contains generic information with an added count field.

    Attributes:
        count:
    """

    count: int


class IssueEntry(GenericEntry):
    """
    The IssueEntry object contains generic information with an added number field.

    Attributes:
        number:
    """

    number: Optional[str] = Field(default=None, alias="issue_number")


class CreatorEntry(GenericEntry):
    r"""
    The CreatorEntry object contains generic information with an added roles field.

    Attributes:
        roles: List of roles used by the Creator, separated by `~\r\n`
    """

    roles: str = Field(alias="role")

    @property
    def role_list(self) -> List[str]:
        r"""
        List of roles the Creator has used.

        Returns:
            List of roles, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.roles) if self.roles else []


class ImageEntry(BaseModel):
    """
    The ImageEntry object contains image information.

    Attributes:
        icon: Url to image of Icon size.
        medium: Url to image of Medium size.
        screen: Url to image of Screen size.
        screen_large: Url to image of Screen Large size.
        small: Url to image of Small size.
        super: Url to image of Super size.
        thumbnail: Url to image of Thumbnail size.
        tiny: Url to image of Tiny size.
        original: Url to image of Original size.
        tags:
    """

    icon: str = Field(alias="icon_url")
    medium: str = Field(alias="medium_url")
    screen: str = Field(alias="screen_url")
    screen_large: str = Field(alias="screen_large_url")
    small: str = Field(alias="small_url")
    super: str = Field(alias="super_url")
    thumbnail: str = Field(alias="thumb_url")
    tiny: str = Field(alias="tiny_url")
    original: str = Field(alias="original_url")
    tags: Optional[str] = Field(default=None, alias="image_tags")
