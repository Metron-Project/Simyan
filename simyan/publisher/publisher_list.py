"""
The PublisherList module.

This module provides the following classes:

- PublisherList
- PublisherResult
- PublisherResultSchema
"""
from typing import Any, Dict, List

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from simyan.exceptions import APIError
from simyan.generic_entries import ImageEntrySchema


class PublisherResult:
    r"""
    The PublisherResult object contains information for a publisher.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Publisher has used, separated by ``\n``.
        api_url (str): Url to the ComicVine API.
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
        summary (str, Optional): Short description of the Publisher.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class PublisherResultSchema(Schema):
    """Schema for the PublisherResult API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
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
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> PublisherResult:
        """
        Make the PublisherResult object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A PublisherResult object
        """
        return PublisherResult(**data)


class PublisherList:
    """
    The PublisherList object contains a list of PublisherResult objects.

    Args:
        response: List of responses returned from ComicVine
    """

    def __init__(self, response: List[Dict[str, Any]]):
        self.publishers = []

        schema = PublisherResultSchema()
        for entry in response:
            try:
                result = schema.load(entry)
            except ValidationError as error:
                raise APIError(error)

            self.publishers.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.publishers)

    def __len__(self):
        """Return the length of the object."""
        return len(self.publishers)

    def __getitem__(self, index: int):
        """Return the result object at the passed index."""
        return self.publishers[index]
