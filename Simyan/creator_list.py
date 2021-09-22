"""
CreatorList module.

This module provides the following classes:

- CreatorResult
- CreatorResultSchema
- CreatorList
"""
from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import ImageEntrySchema


class CreatorResult:
    """
    The CreatorResult object.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new CreatorResult."""
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
        """Any unknown fields will be exclude."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data, **kwargs) -> CreatorResult:
        """
        Make the CreatorResult object.

        :param data: Data from the Comic Vine reponse.

        :returns: :class:`CreatorResult` object
        :rtype: CreatorResult
        """
        return CreatorResult(**data)


class CreatorList:
    """The CreatorList object contains a list of `CreatorResult` objects."""

    def __init__(self, response):
        """Initialize a new CreatorList."""
        self.creators = []

        schema = CreatorResultSchema()
        for iss_dict in response:
            try:
                result = schema.load(iss_dict)
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
        """Return the object of a at index."""
        return self.creators[index]
