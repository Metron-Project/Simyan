"""
The GenericEntries module.

This module provides the following classes:

- GenericEntry
- CountEntry
- IssueEntry
- CreatorEntry
- ImageEntry
"""
from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import Undefined, config, dataclass_json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GenericEntry:
    """The GenericEntry object contains generic information."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the ComicVine API.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in ComicVine.
    name: Optional[str] = field(default=None)
    site_url: Optional[str] = field(
        default=None, metadata=config(field_name="site_detail_url")
    )  #: Url to the ComicVine Website.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CountEntry:
    """The CountEntry object contains generic information with an added count field."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the ComicVine API.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in ComicVine.
    count: int
    name: Optional[str] = field(default=None)
    site_url: Optional[str] = field(
        default=None, metadata=config(field_name="site_detail_url")
    )  #: Url to the ComicVine Website.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class IssueEntry:
    """The IssueEntry object contains generic information with an added number field."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the ComicVine API.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in ComicVine.
    name: Optional[str] = field(default=None)
    number: Optional[str] = field(default=None, metadata=config(field_name="issue_number"))
    site_url: Optional[str] = field(
        default=None, metadata=config(field_name="site_detail_url")
    )  #: Url to the ComicVine Website.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CreatorEntry:
    """The CreatorEntry object contains generic information with an added roles field."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the ComicVine API.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in ComicVine.
    roles: str = field(metadata=config(field_name="role"))  #: separated by ``\n``.
    name: Optional[str] = field(default=None)
    site_url: Optional[str] = field(
        default=None, metadata=config(field_name="site_detail_url")
    )  #: Url to the ComicVine Website.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ImageEntry:
    """The ImageEntry object contains image information."""

    icon: str = field(metadata=config(field_name="icon_url"))  #: Url to image of Icon size.
    medium: str = field(metadata=config(field_name="medium_url"))  #: Url to image of Medium size.
    screen: str = field(metadata=config(field_name="screen_url"))  #: Url to image of Screen size.
    screen_large: str = field(
        metadata=config(field_name="screen_large_url")
    )  #: Url to image of Screen Large size.
    small: str = field(metadata=config(field_name="small_url"))  #: Url to image of Small size.
    super: str = field(metadata=config(field_name="super_url"))  #: Url to image of Super size.
    thumbnail: str = field(
        metadata=config(field_name="thumb_url")
    )  #: Url to image of Thumbnail size.
    tiny: str = field(metadata=config(field_name="tiny_url"))  #: Url to image of Tiny size.
    original: str = field(
        metadata=config(field_name="original_url")
    )  #: Url to image of Original size.
    tags: Optional[str] = field(default=None, metadata=config(field_name="image_tags"))
