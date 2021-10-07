"""
The CharacterList module.

This module provides the following classes:

- CharacterList
- CharacterResult
- CharacterResultSchema
"""
from typing import Any, Dict, List

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from simyan.exceptions import APIError
from simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class CharacterResult:
    r"""
    The CharacterResult object contains information for a character.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Character has used, separated by ``\n``.
        api_url (str): Url to the ComicVine API.
        date_added (datetime): Date and time when the Character was added to ComicVine.
        date_last_updated (datetime): Date and time when the Character was updated on ComicVine.
        date_of_birth (date, Optional): Date when the Character was born.
        description (str): Long description of the Character.
        first_issue (IssueEntry`): First issue the Character appeared in.
        gender (int): Character gender.
        id (int): Identifier used in ComicVine.
        image (ImageEntry): Different sized images, posters and thumbnails for the Character.
        issue_count (int, Optional): Number of issues the Character appears in.
        name (str): Real name or public identity of Character.
        origin (GenericEntry): The type of Character.
        publisher (GenericEntry): The publisher of the Character.
        real_name (str): Name of the Character.
        site_url (str): Url to the ComicVine Website.
        summary (str, Optional): Short description of the Character.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CharacterResultSchema(Schema):
    """Schema for the CharacterResult API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    date_of_birth = fields.Date(data_key="birth", allow_none=True)
    description = fields.Str()
    first_issue = fields.Nested(IssueEntrySchema, data_key="first_appeared_in_issue")
    gender = fields.Int()
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_issue_appearances", allow_none=True)
    name = fields.Str()
    origin = fields.Nested(GenericEntrySchema)
    publisher = fields.Nested(GenericEntrySchema)
    real_name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> CharacterResult:
        """
        Make the CharacterResult object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A CharacterResult object
        """
        return CharacterResult(**data)


class CharacterList:
    """
    The CharacterList object contains a list of CharacterResult objects.

    Args:
        response: List of responses returned from ComicVine
    """

    def __init__(self, response: List[Dict[str, Any]]):
        self.characters = []

        schema = CharacterResultSchema()
        for entry in response:
            try:
                result = schema.load(entry)
            except ValidationError as error:
                raise APIError(error)

            self.characters.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.characters)

    def __len__(self):
        """Return the length of the object."""
        return len(self.characters)

    def __getitem__(self, index: int):
        """Return the result object at the passed index."""
        return self.characters[index]
