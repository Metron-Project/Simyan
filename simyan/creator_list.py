"""
The CreatorList module.

This module provides the following classes:

- CreatorList
- CreatorResult
- CreatorResultSchema
"""
from typing import Any, Dict, List

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from simyan.exceptions import APIError
from simyan.generic_entries import ImageEntrySchema


class CreatorResult:
    r"""
    The CreatorResult object contains information for a creator.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Creator has used, separated by ``\n``.
        api_url (str): Url to the Creator on the ComicVine API.
        country (str): Country where the Creator is from.
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
        name (str): Name of the Creator.
        site_url (str): Url to the Creator on the ComicVine Website.
        summary (str, Optional): Short description of the Creator.
        website (str, Optional): Url to the Creator's website.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorResultSchema(Schema):
    """Schema for the CreatorResult API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    country = fields.Str()
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    date_of_birth = fields.Date(data_key="birth", allow_none=True)
    date_of_death = fields.Date(data_key="death", allow_none=True)
    description = fields.Str()
    email = fields.Str(allow_none=True)
    gender = fields.Int()
    hometown = fields.Str(allow_none=True)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_isssue_appearances", allow_none=True)
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    summary = fields.Str(data_key="deck", allow_none=True)
    website = fields.Str(allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> CreatorResult:
        """
        Make the CreatorResult object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A CreatorResult object
        """
        return CreatorResult(**data)


class CreatorList:
    """
    The CreatorList object contains a list of CreatorResult objects.

    Args:
        response: List of responses returned from ComicVine
    """

    def __init__(self, response: List[Dict[str, Any]]):
        self.creators = []

        schema = CreatorResultSchema()
        for entry in response:
            try:
                result = schema.load(entry)
            except ValidationError as error:
                raise APIError(error)

            self.creators.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.creators)

    def __len__(self):
        """Return the length of the object."""
        return len(self.creators)

    def __getitem__(self, index: int):
        """Return the result object at the passed index."""
        return self.creators[index]
