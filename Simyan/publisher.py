"""
Publisher module.

This module provides the following classes:

- Publisher
- PublisherSchema
"""
from marshmallow import EXCLUDE, Schema, fields, post_load

from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema


class Publisher:
    """
    The Publisher object contains information for publishers.

    :param `**kwargs`: The keyword arguments is used for setting publisher data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new Publisher."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class PublisherSchema(Schema):
    """Schema for the Publisher API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    characters = fields.Nested(GenericEntrySchema, many=True)
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    description = fields.Str(allow_none=True)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    location_address = fields.Str(allow_none=True)
    location_city = fields.Str(allow_none=True)
    location_state = fields.Str(allow_none=True)
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    story_arcs = fields.Nested(GenericEntrySchema, data_key="story_arcs", many=True)
    summary = fields.Str(data_key="deck", allow_none=True)
    teams = fields.Nested(GenericEntrySchema, many=True)
    volumes = fields.Nested(GenericEntrySchema, many=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data, **kwargs) -> Publisher:
        """
        Make the arc object.

        :param data: Data from Comic Vine reponse.

        :returns: :class:`Publisher` object
        :rtype: Publisher
        """
        return Publisher(**data)
