"""
VolumeList module.

This module provides the following classes:

- VolumeResult
- VolumeResultSchema
- VolumeList
"""
from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class VolumeResult:
    """
    The VolumeResult object contains information for comic volumes.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new VolumeResult."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class VolumeResultSchema(Schema):
    """Schema for the VolumeResult API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    description = fields.Str(allow_none=True)
    first_issue = fields.Nested(IssueEntrySchema)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_issues")
    last_issue = fields.Nested(IssueEntrySchema)
    name = fields.Str()
    publisher = fields.Nested(GenericEntrySchema)
    site_url = fields.Url(data_key="site_detail_url")
    start_year = fields.Int()
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        """Any unknown fields will be included."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data, **kwargs) -> VolumeResult:
        """
        Make the VolumeResult object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`VolumeResult` object
        :rtype: VolumeResult
        """
        return VolumeResult(**data)


class VolumeList:
    """The VolumeList object contains a list of `VolumeResult` objects."""

    def __init__(self, response):
        """Initialize a new VolumeList."""
        self.volumes = []

        schema = VolumeResultSchema()
        for vol_dict in response:
            try:
                result = schema.load(vol_dict)
            except ValidationError as error:
                raise APIError(error)

            self.volumes.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.volumes)

    def __len__(self):
        """Return the length of the object."""
        return len(self.volumes)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.volumes[index]
