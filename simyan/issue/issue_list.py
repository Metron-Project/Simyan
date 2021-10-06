"""
The IssueList module.

This module provides the following classes:

- IssueList
- IssueResult
- IssueResultSchema
"""
from typing import Any, Dict, List

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from simyan.exceptions import APIError
from simyan.generic_entries import GenericEntrySchema, ImageEntrySchema


class IssueResult:
    r"""
    The IssueResult object contains information for an issue.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Issue has used, separated by ``\n``.
        api_url (str): Url to the ComicVine API.
        cover_date (date): Date on the cover of the Issue.
        date_added (datetime): Date and time when the Issue was added to ComicVine.
        date_last_updated (datetime): Date and time when the Issue was updated on ComicVine.
        description (str): Long description of the Issue.
        id (int): Identifier used in ComicVine.
        image (ImageEntry): Different sized images, posters and thumbnails for the Issue.
        name (str): Name/Title of the Issue.
        number (str): The Issue number.
        site_url (str): Url to the ComicVine Website.
        store_date (date, Optional): Date the Issue went on sale on stores.
        summary (str, Optional): Short description of the Issue.
        volume (GenericEntry): The volume the Issue is in.
    """

    def __init__(self, **kwargs):
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
    def make_object(self, data: Dict[str, Any], **kwargs) -> IssueResult:
        """
        Make the IssueResult object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            An IssueResult object
        """
        return IssueResult(**data)


class IssueList:
    """
    The IssueList object contains a list of IssueResult objects.

    Args:
        response: List of responses returned from ComicVine
    """

    def __init__(self, response: List[Dict[str, Any]]):
        self.issues = []

        schema = IssueResultSchema()
        for entry in response:
            try:
                result = schema.load(entry)
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
        """Return the result object at the passed index."""
        return self.issues[index]
