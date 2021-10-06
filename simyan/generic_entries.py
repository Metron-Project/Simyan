"""
The GenericEntries module.

This module provides the following classes:

- GenericEntry
- GenericEntrySchema
- CountEntry
- CountEntrySchema
- IssueEntry
- IssueEntrySchema
- CreatorEntry
- CreatorEntrySchema
- ImageEntry
- ImageEntrySchema
"""
from typing import Any, Dict

from marshmallow import EXCLUDE, Schema, fields, post_load


class GenericEntry:
    """
    The GenericEntry object contains generic information.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        api_url (str): Url to the ComicVine API.
        id (int): Identifier used in ComicVine.
        name (str):
        site_url (str): Url to the ComicVine Website.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class GenericEntrySchema(Schema):
    """Schema for the GenericEntry data."""

    api_url = fields.Url(data_key="api_detail_url")
    id = fields.Int()
    name = fields.Str(allow_none=True)
    site_url = fields.Url(data_key="site_detail_url", allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> GenericEntry:
        """
        Make the GenericEntry object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A `GenericEntry` object
        """
        return GenericEntry(**data)


class CountEntry:
    """
    The CountEntry object contains generic information with an added count field.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        api_url (str): Url to the ComicVine API.
        id (int): Identifier used in ComicVine.
        name (str):
        site_url (str): Url to the ComicVine Website.
        count (int):
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CountEntrySchema(GenericEntrySchema):
    """Schema for the CountEntry data."""

    count = fields.Int()

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> CountEntry:
        """
        Make the CountEntry object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A `CountEntry` object
        """
        return CountEntry(**data)


class IssueEntry:
    """
    The IssueEntry object contains generic information with an added number field.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        api_url (str): Url to the ComicVine API.
        id (int): Identifier used in ComicVine.
        name (str):
        site_url (str): Url to the ComicVine Website.
        number (str, Optional):
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueEntrySchema(GenericEntrySchema):
    """Schema for the IssueEntry data."""

    number = fields.Str(data_key="issue_number", allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> IssueEntry:
        """
        Make the IssueEntry object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            An `IssueEntry` object
        """
        return IssueEntry(**data)


class CreatorEntry:
    r"""
    The CreatorEntry object contains generic information with an added roles field.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        api_url (str): Url to the ComicVine API.
        id (int): Identifier used in ComicVine.
        name (str):
        site_url (str): Url to the ComicVine Website.
        roles (str): separated by ``\n``
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorEntrySchema(GenericEntrySchema):
    """Schema for the CreatorEntry data."""

    roles = fields.Str(data_key="role")

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> CreatorEntry:
        """
        Make the CreatorEntry object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A `CreatorEntry` object
        """
        return CreatorEntry(**data)


class ImageEntry:
    """
    The ImageEntry object contains image information.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        icon (str): Url to image of Icon size.
        medium (str): Url to image of Medium size.
        screen (str): Url to image of Screen size.
        screen_large (str): Url to image of Screen Large size.
        small (str): Url to image of Small size.
        super (str): Url to image of Super size.
        thumb (str): Url to image of Thumbnail size.
        tiny (str): Url to image of Tiny size.
        original (str): Url to image of Original size.
        tags (str, Optional):
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ImageEntrySchema(Schema):
    """Schema for the ImageEntry data."""

    icon = fields.Url(data_key="icon_url")
    medium = fields.Url(data_key="medium_url")
    screen = fields.Url(data_key="screen_url")
    screen_large = fields.Url(data_key="screen_large_url")
    small = fields.Url(data_key="small_url")
    super = fields.Url(data_key="super_url")
    thumb = fields.Url(data_key="thumb_url")
    tiny = fields.Url(data_key="tiny_url")
    original = fields.Url(data_key="original_url")
    tags = fields.Str(data_key="image_tags", allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> ImageEntry:
        """
        Make the ImageEntry object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            An `ImageEntry` object
        """
        return ImageEntry(**data)
