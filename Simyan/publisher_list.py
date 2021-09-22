"""
PublishersList module.

This module provides the following classes:

- PublisherResult
- PublisherResultSchema
- PublishersList
"""
from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import ImageEntrySchema


class PublisherResult:
    """
    The PublisherResult object contains information for a publisher.

    :param `**kwargs`: The keyword arguments is used for setting publisher data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new PublisherResult."""
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
    def make_object(self, data, **kwargs) -> PublisherResult:
        """
        Make the PublisherResult object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`PublisherResult` object
        :rtype: PublisherResult
        """
        return PublisherResult(**data)


class PublisherList:
    """The PublishersList object contains a list of `PublisherResult` objects."""

    def __init__(self, response):
        """Initialize a new PublishersList."""
        self.publishers = []

        schema = PublisherResultSchema()
        for pub_dict in response:
            try:
                result = schema.load(pub_dict)
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
        """Return the object of a at index."""
        return self.publishers[index]
