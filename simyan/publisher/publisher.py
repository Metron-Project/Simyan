"""
The Publisher module.

This module provides the following classes:

- Publisher
- PublisherSchema
"""
from typing import Any, Dict

from marshmallow import EXCLUDE, Schema, fields, post_load

from simyan.generic_entries import GenericEntrySchema, ImageEntrySchema


class Publisher:
    r"""
    The Publisher object contains information for a publisher.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Publisher has used, separated by ``\n``.
        api_url (str): Url to the ComicVine API.
        characters (list[GenericEntry]): List of characters the Publisher created.
        date_added (datetime): Date and time when the Publisher was added to ComicVine.
        date_last_updated (datetime): Date and time when the Publisher was updated on ComicVine.
        description (str): Long description of the Publisher.
        id (int): Identifier used in ComicVine.
        image (ImageEntry): Different sized images, posters and thumbnails for the Publisher.
        location_address (str, Optional): Address of the Publisher.
        location_city (str, Optional): City where the Publisher is.
        location_state (str, Optional): State where the Publisher is.
        name (str): Name/Title of the Publisher.
        site_url (str): Url to the ComicVine Website.
        story_arcs (list[GenericEntry]): List of story arcs the Publisher created.
        summary (str, Optional): Short description of the Publisher.
        teams (list[GenericEntry]): List of teams the Publisher created.
        volumes (list[GenericEntry]): List of volumes the Publisher created.
    """

    def __init__(self, **kwargs):
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
    def make_object(self, data: Dict[str, Any], **kwargs) -> Publisher:
        """
        Make the Publisher object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A Publisher object
        """
        return Publisher(**data)
