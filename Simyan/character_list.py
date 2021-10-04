"""
CharacterList module.

This module provides the following classes:

- CharacterResult
- CharacterResultSchema
- CharacterList
"""
from typing import Any, Dict, List

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class CharacterResult:
    """
    The CharacterResult object.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Initialize a new CharacterResult."""
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
    first_issue = fields.Nested(IssueEntrySchema)
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
    def make_object(self, data, **kwargs) -> CharacterResult:
        """
        Make the CharacterResult object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`CharacterResult` object
        :rtype: CharacterResult
        """
        return CharacterResult(**data)


class CharacterList:
    """The CharacterList object contains a list of `CharacterResult` objects."""

    def __init__(self, response: List[Dict[str, Any]]):
        """
        Initialize a new CharacterList.

        :param response: List of responses returned from Comicvine
        :type response: List
        """
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
