"""
Creator module.

This module provides the following classes:

- Creator
- CreatorSchema
"""
from marshmallow import EXCLUDE, Schema, fields, post_load, pre_load

from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema


class Creator:
    """
    The Creator object contains information for creators.

    :param `**kwargs`: The keyword arguments is used for setting creator data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new Creator."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorSchema(Schema):
    """Schema for the Creator API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    country = fields.Str()
    created_characters = fields.Nested(GenericEntrySchema, many=True)
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    date_of_birth = fields.Date(data_key="birth", allow_none=True)
    date_of_death = fields.Date(format="%Y-%m-%d %H:%M:%S.%f", data_key="death", allow_none=True)
    description = fields.Str()
    email = fields.Str(allow_none=True)
    gender = fields.Int()
    hometown = fields.Str(allow_none=True)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_isssue_appearances", allow_none=True)
    issues = fields.Nested(GenericEntrySchema, many=True)
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    story_arcs = fields.Nested(GenericEntrySchema, data_key="story_arc_credits", many=True)
    summary = fields.Str(data_key="deck", allow_none=True)
    volumes = fields.Nested(GenericEntrySchema, data_key="volume_credits", many=True)
    website = fields.Str(allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @pre_load
    def process_input(self, data, **kwargs):
        """
        Only keep the date of death information from Comic Vine.

        The time zone info they include is not of any use.

        :param data: Data from the Comic Vine response
        """
        new_data = data

        if "death" in new_data and new_data["death"] is not None:
            new_data["death"] = new_data["death"]["date"]

        return new_data

    @post_load
    def make_object(self, data, **kwargs) -> Creator:
        """
        Make the Creator object.

        :param data: Data from Comic Vine reponse.

        :returns: :class:`Creator` object
        :rtype: Creator
        """
        return Creator(**data)
