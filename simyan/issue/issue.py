"""
The Issue module.

This module provides the following classes:

- Issue
- IssueSchema
"""
from typing import Any, Dict

from marshmallow import EXCLUDE, Schema, fields, post_load

from simyan.generic_entries import CreatorEntrySchema, GenericEntrySchema, ImageEntrySchema


class Issue:
    r"""
    The Issue object contains information for an issue.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Issue has used, separated by ``\n``.
        api_url (str): Url to the ComicVine API.
        character_deaths (list[GenericEntry]): List of characters who died in the Issue.
        characters (list[GenericEntry]): List of characters in the Issue.
        concepts (list[GenericEntry]): List of concepts in the Issue.
        cover_date (date): Date on the cover of the Issue.
        creators (list[GenericEntry]): List of creators which worked on the Issue.
        date_added (datetime): Date and time when the Issue was added to ComicVine.
        date_last_updated (datetime): Date and time when the Issue was updated on ComicVine.
        description (str): Long description of the Issue.
        first_appearance_characters (Optional, list[GenericEntry]):
            List of characters who first appear in the Issue.
        first_appearance_concepts (Optional, list[GenericEntry]):
            List of concepts which first appear in the Issue.
        first_appearance_locations (Optional, list[GenericEntry]):
            List of locations which first appear in the Issue.
        first_appearance_objects (Optional, list[GenericEntry]):
            List of objects which first appear in the Issue.
        first_appearance_story_arcs (Optional, list[GenericEntry]):
            List of story arcs which start in the Issue.
        first_appearance_teams (Optional, list[GenericEntry]):
            List of teams which first appear in the Issue.
        id (int): Identifier used in ComicVine.
        image (ImageEntry): Different sized images, posters and thumbnails for the Issue.
        locations (list[GenericEntry]): List of locations which appear in the Issue.
        name (str): Name/Title of the Issue.
        number (str): The Issue number.
        objects (list[GenericEntry]): List of objects which appear in the Issue.
        site_url (str): Url to the ComicVine Website.
        store_date (date, Optional): Date the Issue went on sale on stores.
        story_arcs (list[GenericEntry]): List of story arcs the Issue appears in.
        summary (str, Optional): Short description of the Issue.
        teams (list[GenericEntry]): List of teams which appear in the Issue.
        teams_disbanded (list[GenericEntry]): List of teams which disbanded in the Issue.
        volume (GenericEntry): The volume the Issue is in.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueSchema(Schema):
    """Schema for the Issue API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    characters = fields.Nested(GenericEntrySchema, data_key="character_credits", many=True)
    concepts = fields.Nested(GenericEntrySchema, data_key="concept_credits", many=True)
    cover_date = fields.Date()
    creators = fields.Nested(CreatorEntrySchema, data_key="person_credits", many=True)
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    deaths = fields.Nested(GenericEntrySchema, data_key="character_died_in", many=True)
    description = fields.Str()
    first_appearance_characters = fields.Nested(GenericEntrySchema, allow_none=True, many=True)
    first_appearance_concepts = fields.Nested(GenericEntrySchema, allow_none=True, many=True)
    first_appearance_locations = fields.Nested(GenericEntrySchema, allow_none=True, many=True)
    first_appearance_objects = fields.Nested(GenericEntrySchema, allow_none=True, many=True)
    first_appearance_story_arcs = fields.Nested(
        GenericEntrySchema, data_key="first_appearance_storyarcs", allow_none=True, many=True
    )
    first_appearance_teams = fields.Nested(GenericEntrySchema, allow_none=True, many=True)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    locations = fields.Nested(GenericEntrySchema, data_key="location_credits", many=True)
    name = fields.Str(allow_none=True)
    number = fields.Str(data_key="issue_number")
    objects = fields.Nested(GenericEntrySchema, data_key="object_credits", many=True)
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
    def make_object(self, data: Dict[str, Any], **kwargs) -> Issue:
        """
        Make the Issue object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            An Issue object
        """
        return Issue(**data)
