"""
The GenericEntries module.

This module provides the following classes:

- GenericEntry
- CountEntry
- IssueEntry
- CreatorEntry
- ImageEntry
"""
from typing import Optional

from pydantic import BaseModel, Field


class GenericEntry(BaseModel):
    """The GenericEntry object contains generic information."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    id_: int = Field(alias="id")  #: Identifier used in Comicvine.
    name: Optional[str] = None
    site_url: Optional[str] = Field(alias="site_detail_url")  #: Url to the Comicvine Website.


class CountEntry(BaseModel):
    """The CountEntry object contains generic information with an added count field."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    id_: int = Field(alias="id")  #: Identifier used in Comicvine.
    count: int
    name: Optional[str] = None
    site_url: Optional[str] = Field(
        default=None, alias="site_detail_url"
    )  #: Url to the Comicvine Website.


class IssueEntry(BaseModel):
    """The IssueEntry object contains generic information with an added number field."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    id_: int = Field(alias="id")  #: Identifier used in Comicvine.
    name: Optional[str] = None
    number: Optional[str] = Field(default=None, alias="issue_number")
    site_url: Optional[str] = Field(
        default=None, alias="site_detail_url"
    )  #: Url to the Comicvine Website.


class CreatorEntry(BaseModel):
    """The CreatorEntry object contains generic information with an added roles field."""

    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    id_: int = Field(alias="id")  #: Identifier used in Comicvine.
    roles: str = Field(alias="role")  #: separated by ``\n``.
    name: Optional[str] = None
    site_url: Optional[str] = Field(
        default=None, alias="site_detail_url"
    )  #: Url to the Comicvine Website.


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
