"""
Character module.

This module provides the following classes:

- Character
- CharacterSchema
"""
from marshmallow import EXCLUDE, Schema, fields, post_load

from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class Character:
    """
    The Character object contains information for characters.

    :param `**kwargs`: The keyword arguments is used for setting character data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Initialize a new Character."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class CharacterSchema(Schema):
    """Schema for the Character API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    creators = fields.Nested(GenericEntrySchema, many=True)
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    date_of_birth = fields.Date(data_key="birth", allow_none=True)
    deaths = fields.Nested(GenericEntrySchema, data_key="issues_died_in", many=True)
    description = fields.Str()
    enemies = fields.Nested(GenericEntrySchema, data_key="character_enemies", many=True)
    enemy_teams = fields.Nested(GenericEntrySchema, data_key="team_enemies", many=True)
    first_issue = fields.Nested(IssueEntrySchema)
    friend_teams = fields.Nested(GenericEntrySchema, data_key="team_friends", many=True)
    friends = fields.Nested(GenericEntrySchema, data_key="character_friends", many=True)
    gender = fields.Int()
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_appearances = fields.Nested(GenericEntrySchema, data_key="issue_credits", many=True)
    issue_count = fields.Int(data_key="count_of_issue_appearances", allow_none=True)
    name = fields.Str()
    origin = fields.Nested(GenericEntrySchema)
    powers = fields.Nested(GenericEntrySchema, many=True)
    publisher = fields.Nested(GenericEntrySchema)
    real_name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    story_arc_appearances = fields.Nested(GenericEntrySchema, data_key="story_arc_credits", many=True)
    summary = fields.Str(data_key="deck", allow_none=True)
    teams = fields.Nested(GenericEntrySchema, many=True)
    volume_appearances = fields.Nested(GenericEntrySchema, data_key="volume_credits", many=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data, **kwargs) -> Character:
        """
        Make the Character object.

        :param data: Data from Comic Vine response.

        :returns: :class:`Character` object
        :rtype: Character
        """
        return Character(**data)
