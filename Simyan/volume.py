"""
Volume module.

This module provides the following classes:

- Volume
- VolumeSchema
"""
from marshmallow import EXCLUDE, Schema, fields, post_load

from Simyan.generic_entries import CountEntrySchema, GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class Volume:
    """
    The Volume object contains information for comic volume.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new Volume."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class VolumeSchema(Schema):
    """Schema for the Volume API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    characters = fields.Nested(CountEntrySchema, many=True)
    concepts = fields.Nested(CountEntrySchema, many=True)
    creators = fields.Nested(CountEntrySchema, data_key="people", many=True)
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    description = fields.Str(allow_none=True)
    first_issue = fields.Nested(IssueEntrySchema)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_issues")
    issues = fields.Nested(IssueEntrySchema, many=True)
    last_issue = fields.Nested(IssueEntrySchema)
    locations = fields.Nested(CountEntrySchema, many=True)
    name = fields.Str()
    objects = fields.Nested(CountEntrySchema, many=True)
    publisher = fields.Nested(GenericEntrySchema)
    site_url = fields.Url(data_key="site_detail_url")
    start_year = fields.Int()
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data, **kwargs) -> Volume:
        """
        Make the Volume object.

        :param data: Data from Comic Vine response.

        :returns: :class:`Volume` object
        :rtype: Volume
        """
        return Volume(**data)
