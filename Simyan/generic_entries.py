"""
Generic Entries module.

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
from marshmallow import EXCLUDE, Schema, fields, post_load


class GenericEntry:
    """
    The GenericEntry object contains generic information.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new GenericEntry."""
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
    def make_object(self, data, **kwargs) -> GenericEntry:
        """
        Make the GenericEntry object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`GenericEntry` object
        :rtype: GenericEntry
        """
        return GenericEntry(**data)


class CountEntry:
    """
    The CountEntry object contains count information.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new CountEntry."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class CountEntrySchema(GenericEntrySchema):
    """Schema for the CountEntry data."""

    count = fields.Int()

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> CountEntry:
        """
        Make the CountEntry object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`CountEntry` object
        :rtype: CountEntry
        """
        return CountEntry(**data)


class IssueEntry:
    """
    The IssueEntry object contains count information.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new IssueEntry."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueEntrySchema(GenericEntrySchema):
    """Schema for the IssueEntry data."""

    number = fields.Str(data_key="issue_number", allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> IssueEntry:
        """
        Make the IssueEntry object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`IssueEntry` object
        :rtype: IssueEntry
        """
        return IssueEntry(**data)


class CreatorEntry:
    """
    The CreatorEntry object contains creator role information.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new CreatorEntry."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorEntrySchema(GenericEntrySchema):
    """Schema for the CreatorEntry data."""

    roles = fields.Str(data_key="role")

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> CreatorEntry:
        """
        Make the CreatorEntry object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`CreatorEntry` object
        :rtype: CreatorEntry
        """
        return CreatorEntry(**data)


class ImageEntry:
    """
    The ImageEntry object contains image information.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new ImageEntry."""
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
    def make_object(self, data, **kwargs) -> ImageEntry:
        """
        Make the ImageEntry object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`ImageEntry` object
        :rtype: ImageEntry
        """
        return ImageEntry(**data)
