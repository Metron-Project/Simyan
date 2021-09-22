"""
StoryArc module.

This module provides the following classes:

- StoryArc
- StoryArcSchema
"""
from marshmallow import EXCLUDE, Schema, fields, post_load

from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class StoryArc:
    """
    The StoryArc object contains information for story arcs.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new StoryArc."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class StoryArcSchema(Schema):
    """Schema for the StoryArc API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    description = fields.Str(allow_none=True)
    # Ignoring Episodes
    # Ignoring First Episode
    first_issue = fields.Nested(IssueEntrySchema, data_key="first_appeared_in_issue")
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_isssue_appearances")
    issues = fields.Nested(GenericEntrySchema, many=True)
    # Ignoring Movies
    name = fields.Str()
    publisher = fields.Nested(GenericEntrySchema)
    site_url = fields.Url(data_key="site_detail_url")
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data, **kwargs) -> StoryArc:
        """
        Make the story arc object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`StoryArc` object
        :rtype: StoryArc
        """
        return StoryArc(**data)
