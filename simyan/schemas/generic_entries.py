"""The GenericEntries module.

This module provides the following classes:

- GenericEntry
- CountEntry
- IssueEntry
- CreatorEntry
- Image
- AssociatedImage
"""
__all__ = [
    "GenericEntry",
    "CountEntry",
    "IssueEntry",
    "CreatorEntry",
    "Image",
    "AssociatedImage",
]
from typing import Optional

from pydantic import Field

from simyan.schemas import BaseModel


class GenericEntry(BaseModel, extra="forbid"):
    """The GenericEntry object contains generic information.

    Attributes:
        api_url: Url to the resource in the Comicvine API.
        id: Identifier used by Comicvine.
        name:
        site_url: Url to the resource in Comicvine.
    """

    api_url: str = Field(alias="api_detail_url")
    id: int  # noqa: A003
    name: Optional[str] = None
    site_url: Optional[str] = Field(default=None, alias="site_detail_url")


class CountEntry(GenericEntry):
    r"""Extends GenericEntry by including attributes for tracking counts.

    Attributes:
        count:
    """

    count: int


class IssueEntry(GenericEntry):
    r"""Extends GenericEntry by including attributes of an Issue.

    Attributes:
        number:
    """

    number: Optional[str] = Field(default=None, alias="issue_number")


class CreatorEntry(GenericEntry):
    r"""Extends GenericEntry by including attributes of a Creator.

    Attributes:
        roles: List of roles used by the Creator, collected in a string.
    """

    roles: str = Field(alias="role")


class Image(BaseModel, extra="forbid"):
    """The Image object contains image information.

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

    icon_url: str
    large_screen_url: str = Field(alias="screen_large_url")
    medium_url: str
    original_url: str
    screen_url: str
    small_url: str
    super_url: str
    thumbnail: str = Field(alias="thumb_url")
    tiny_url: str
    tags: Optional[str] = Field(default=None, alias="image_tags")


class AssociatedImage(BaseModel, extra="forbid"):
    """The AssociatedImage object contains image information.

    Attributes:
        url: Url to image.
        id: Identifier used by Comicvine.
        caption: Caption/description of the image.
        tags:
    """

    url: str = Field(alias="original_url")
    id: int  # noqa: A003
    caption: Optional[str] = None
    tags: Optional[str] = Field(default=None, alias="image_tags")
