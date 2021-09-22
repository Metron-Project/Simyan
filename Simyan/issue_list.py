"""
IssuesList module.

This module provides the following classes:

- IssueResult
- IssueResultSchema
- IssuesList
"""
from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema


class IssueResult:
    """
    The IssueResult object contains information for an issue.

    :param `**kwargs`: The keyword arguments is used for setting issue data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new IssueResult."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueResultSchema(Schema):
    """Schema for the IssueResult API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    cover_date = fields.Date()
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    description = fields.Str()
    # Ignoring has_staff_review
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    name = fields.Str(allow_none=True)
    number = fields.Str(data_key="issue_number")
    site_url = fields.Url(data_key="site_detail_url")
    store_date = fields.Date(allow_none=True)
    summary = fields.Str(data_key="deck", allow_none=True)
    volume = fields.Nested(GenericEntrySchema)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data, **kwargs) -> IssueResult:
        """
        Make the IssueResult object.

        :param data: Data from Comic Vine response.

        :returns: :class:`IssueResult` object
        :rtype: IssueResult
        """
        return IssueResult(**data)


class IssueList:
    """The IssuesList object contains a list of `IssueResult` objects."""

    def __init__(self, response):
        """Initialize a new IssuesList."""
        self.issues = []

        schema = IssueResultSchema()
        for iss_dict in response:
            try:
                result = schema.load(iss_dict)
            except ValidationError as error:
                raise APIError(error)

            self.issues.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.issues)

    def __len__(self):
        """Return the length of the object."""
        return len(self.issues)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.issues[index]
