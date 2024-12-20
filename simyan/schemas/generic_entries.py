"""The GenericEntries module.

This module provides the following classes:
- AssociatedImage
- GenericCount
- GenericCreator
- GenericEntry
- GenericIssue
- Images
"""

__all__ = [
    "AssociatedImage",
    "GenericCount",
    "GenericCreator",
    "GenericEntry",
    "GenericIssue",
    "Images",
]

from typing import Optional

from pydantic import Field, HttpUrl

from simyan.schemas import BaseModel


class GenericEntry(BaseModel, extra="forbid"):
    """The GenericEntry object contains generic information.

    Attributes:
        api_url: Url to the resource in the Comicvine API.
        id: Identifier used by Comicvine.
        name:
        site_url: Url to the resource in Comicvine.
    """

    api_url: HttpUrl = Field(alias="api_detail_url")
    id: int
    name: Optional[str] = None
    site_url: Optional[HttpUrl] = Field(default=None, alias="site_detail_url")


class GenericCount(GenericEntry):
    r"""Extends GenericEntry by including attributes for tracking counts.

    Attributes:
        count:
    """

    count: int


class GenericIssue(GenericEntry):
    r"""Extends GenericEntry by including attributes of an Issue.

    Attributes:
        number:
    """

    number: Optional[str] = Field(default=None, alias="issue_number")


class GenericCreator(GenericEntry):
    r"""Extends GenericEntry by including attributes of a Creator.

    Attributes:
        roles: List of roles used by the Creator, collected in a string.
    """

    roles: str = Field(alias="role")


class Images(BaseModel, extra="forbid"):
    """The Images object contains image information.

    Attributes:
        icon_url: Url to an image at icon size.
        large_screen_url: Url to an image at large screen size.
        medium_url: Url to an image at medium size.
        original_url: Url to an image at original size.
        screen_url: Url to an image at screen size.
        small_url: Url to an image at small size.
        super_url: Url to an image at super size.
        thumbnail: Url to an image at thumbnail size.
        tiny_url: Url to an image at tiny size.
        tags:
    """

    icon_url: HttpUrl
    large_screen_url: HttpUrl = Field(alias="screen_large_url")
    medium_url: HttpUrl
    original_url: HttpUrl
    screen_url: HttpUrl
    small_url: HttpUrl
    super_url: HttpUrl
    thumbnail: HttpUrl = Field(alias="thumb_url")
    tiny_url: HttpUrl
    tags: Optional[str] = Field(default=None, alias="image_tags")


class AssociatedImage(BaseModel, extra="forbid"):
    """The AssociatedImage object contains image information.

    Attributes:
        url: Url to image.
        id: Identifier used by Comicvine.
        caption: Caption/description of the image.
        tags:
    """

    url: HttpUrl = Field(alias="original_url")
    id: int
    caption: Optional[str] = None
    tags: Optional[str] = Field(default=None, alias="image_tags")
