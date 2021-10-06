"""
The Creator module.

This module provides the following classes:

- Creator
- CreatorSchema
"""
from typing import Any, Dict

from marshmallow import EXCLUDE, Schema, fields, post_load, pre_load

from simyan.generic_entries import GenericEntrySchema, ImageEntrySchema


class Creator:
    r"""
    The Creator object contains information for a creator.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Creator has used, separated by ``\n``.
        api_url (str): Url to the ComicVine API.
        country (str): Country where the Creator is from.
        characters (list[GenericEntry]): List of characters the Creator has created.
        date_added (datetime): Date and time when the Creator was added to ComicVine.
        date_last_updated (datetime): Date and time when the Creator was updated on ComicVine.
        date_of_birth (date, Optional): Date when the Creator was born.
        date_of_death (date, Optional): Date when the Creator died.
        description (str): Long description of the Creator.
        email (str, Optional): Email address of the Creator.
        gender (int): Creator gender.
        hometown (str, Optional): Hometown of the Creator.
        id (int): Identifier used in ComicVine.
        image (ImageEntry): Different sized images, posters and thumbnails for the Creator.
        issue_count (int, Optional): Number of issues the Creator appears in.
        issues (list[GenericEntry]): List of issues the Creator appears in.
        name (str): Name of the Creator.
        site_url (str): Url to the ComicVine Website.
        story_arcs (list[GenericEntry]): List of story arcs the Creator appears in.
        summary (str, Optional): Short description of the Creator.
        volumes (list[GenericEntry]): List of volumes the Creator appears in.
        website (str, Optional): Url to the Creator's website.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorSchema(Schema):
    """Schema for the Creator API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    country = fields.Str()
    characters = fields.Nested(GenericEntrySchema, data_key="created_characters", many=True)
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
    def process_input(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Only keep the date of death information from ComicVine. The timezone info they include is not of any use.

        Args:
            data: Data from the ComicVine response
            **kwargs:

        Returns:
            ComicVine response with the date of death information included.
        """
        new_data = data

        if "death" in new_data and new_data["death"] is not None:
            new_data["death"] = new_data["death"]["date"]

        return new_data

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> Creator:
        """
        Make the Creator object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A Creator object
        """
        return Creator(**data)
