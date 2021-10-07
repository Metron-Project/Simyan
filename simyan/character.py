"""
The Character module.

This module provides the following classes:

- Character
- CharacterSchema
"""
from typing import Any, Dict

from marshmallow import EXCLUDE, Schema, fields, post_load

from simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class Character:
    r"""
    The Character object contains information for a character.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Character has used, separated by ``\n``.
        api_url (str): Url to the ComicVine API.
        creators (list[GenericEntry]): List of creators which worked on the Character.
        date_added (datetime): Date and time when the Character was added to ComicVine.
        date_last_updated (datetime): Date and time when the Character was updated on ComicVine.
        date_of_birth (date, Optional): Date when the Character was born.
        deaths (list[GenericEntry]): List of times when the Character has died.
        description (str): Long description of the Character.
        enemies (list[GenericEntry]): List of enemies the Character has.
        enemy_teams (list[GenericEntry]): List of enemy teams the Character has.
        first_issue (IssueEntry): First issue the Character appeared in.
        friendly_teams (list[GenericEntry]): List of friendly teams the Character has.
        friends (list[GenericEntry]): List of friends the Character has.
        gender (int): Character gender.
        id (int): Identifier used in ComicVine.
        image (ImageEntry): Different sized images, posters and thumbnails for the Character.
        issue_count (int, Optional): Number of issues the Character appears in.
        issues (list[GenericEntry]): List of issues the Character appears in.
        name (str): Real name or public identity of Character.
        origin (GenericEntry): The type of Character.
        powers (list[GenericEntry]): List of powers the Character has.
        publisher (GenericEntry): The publisher of the Character.
        real_name (str): Name of the Character.
        site_url (str): Url to the ComicVine Website.
        story_arcs (list[GenericEntry]): List of story arcs the Character appears in.
        summary (str, Optional): Short description of the Character.
        teams (list[GenericEntry]): List of teams the Character appears in.
        volumes (list[GenericEntry]): List of volumes the Character appears in.
    """

    def __init__(self, **kwargs):
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
    first_issue = fields.Nested(IssueEntrySchema, data_key="first_appeared_in_issue")
    friendly_teams = fields.Nested(GenericEntrySchema, data_key="team_friends", many=True)
    friends = fields.Nested(GenericEntrySchema, data_key="character_friends", many=True)
    gender = fields.Int()
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_issue_appearances", allow_none=True)
    issues = fields.Nested(GenericEntrySchema, data_key="issue_credits", many=True)
    name = fields.Str()
    origin = fields.Nested(GenericEntrySchema)
    powers = fields.Nested(GenericEntrySchema, many=True)
    publisher = fields.Nested(GenericEntrySchema)
    real_name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    story_arcs = fields.Nested(GenericEntrySchema, data_key="story_arc_credits", many=True)
    summary = fields.Str(data_key="deck", allow_none=True)
    teams = fields.Nested(GenericEntrySchema, many=True)
    volumes = fields.Nested(GenericEntrySchema, data_key="volume_credits", many=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> Character:
        """
        Make the Character object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:
        Returns:
            A Character object
        """
        return Character(**data)
