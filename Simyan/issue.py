"""
Issue module.

This module provides the following classes:

- Issue
- IssueSchema
"""
from marshmallow import EXCLUDE, Schema, fields, post_load

from Simyan.generic_entries import CreatorEntrySchema, GenericEntrySchema, ImageEntrySchema


class Issue:
    """
    The Issue object contains information for an issue.

    :param `**kwargs`: The keyword arguments is used for setting issue data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new Issue."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueSchema(Schema):
    """Schema for the Issue API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    character_deaths = fields.Nested(GenericEntrySchema, data_key="character_died_in", many=True)
    characters = fields.Nested(GenericEntrySchema, data_key="character_credits", many=True)
    concepts = fields.Nested(GenericEntrySchema, data_key="concept_credits", many=True)
    cover_date = fields.Date()
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    description = fields.Str()
    first_appearance_characters = fields.Nested(GenericEntrySchema, allow_none=True)
    first_appearance_concepts = fields.Nested(GenericEntrySchema, allow_none=True)
    first_appearance_locations = fields.Nested(GenericEntrySchema, allow_none=True)
    first_appearance_objects = fields.Nested(GenericEntrySchema, allow_none=True)
    first_appearance_story_arcs = fields.Nested(
        GenericEntrySchema, data_key="first_appearance_storyarcs", allow_none=True
    )
    first_appearance_teams = fields.Nested(GenericEntrySchema, allow_none=True)
    # Ignoring has_staff_review
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    locations = fields.Nested(GenericEntrySchema, data_key="location_credits", many=True)
    name = fields.Str(allow_none=True)
    number = fields.Str(data_key="issue_number")
    items = fields.Nested(GenericEntrySchema, data_key="object_credits", many=True)
    creators = fields.Nested(CreatorEntrySchema, data_key="person_credits", many=True)
    site_url = fields.Url(data_key="site_detail_url")
    store_date = fields.Date(allow_none=True)
    story_arcs = fields.Nested(GenericEntrySchema, data_key="story_arc_credits", many=True)
    summary = fields.Str(data_key="deck", allow_none=True)
    teams = fields.Nested(GenericEntrySchema, data_key="team_credits", many=True)
    teams_disbanded = fields.Nested(GenericEntrySchema, data_key="team_disbanded_in", many=True)
    volume = fields.Nested(GenericEntrySchema)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data, **kwargs) -> Issue:
        """
        Make the issue object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`Issue` object
        :rtype: Issue
        """
        return Issue(**data)
