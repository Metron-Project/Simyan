"""
The VolumeList module.

This module provides the following classes:

- VolumeList
- VolumeResult
- VolumeResultSchema
"""
from typing import Any, Dict, List

from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load, pre_load

from simyan.exceptions import APIError
from simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class VolumeResult:
    r"""
    The VolumeResult object contains information for a volume.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Volume has used, separated by ``\n``.
        api_url (str): Url to the ComicVine API.
        date_added (datetime): Date and time when the Volume was added to ComicVine.
        date_last_updated (datetime): Date and time when the Volume was updated on ComicVine.
        description (str, Optional): Long description of the Volume.
        first_issue (IssueEntry): First issue of the Volume.
        id (int): Identifier used in ComicVine.
        image (ImageEntry): Different sized images, posters and thumbnails for the Volume.
        issue_count (int): Number of issues in the Volume.
        last_issue (IssueEntry): Last issue of the Volume.
        name (str): Name/Title of the Volume.
        publisher (GenericEntry, Optional): The publisher of the Volume.
        site_url (str): Url to the ComicVine Website.
        start_year (int, Optional): The year the Volume started.
        summary (str, Optional): Short description of the Volume.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class VolumeResultSchema(Schema):
    """Schema for the VolumeResult API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    description = fields.Str(allow_none=True)
    first_issue = fields.Nested(IssueEntrySchema)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_issues")
    last_issue = fields.Nested(IssueEntrySchema)
    name = fields.Str()
    publisher = fields.Nested(GenericEntrySchema, allow_none=True)
    site_url = fields.Url(data_key="site_detail_url")
    start_year = fields.Int(allow_none=True)
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        """Any unknown fields will be included."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @pre_load
    def process_input(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Handle non-int values for start_year.

        Args:
            data: Data from the ComicVine response
            **kwargs:

        Returns:
            ComicVine response with the start year either None or Int.
        """
        if "start_year" in data and data["start_year"]:
            try:
                data["start_year"] = int(data["start_year"])
            except ValueError:
                data["start_year"] = None
        return data

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> VolumeResult:
        """
        Make the VolumeResult object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A VolumeResult object
        """
        return VolumeResult(**data)


class VolumeList:
    """
    The VolumeList object contains a list of VolumeResult objects.

    Args:
        response: List of responses returned from ComicVine
    """

    def __init__(self, response: List[Dict[str, Any]]):
        self.volumes = []

        schema = VolumeResultSchema()
        for entry in response:
            try:
                result = schema.load(entry)
            except ValidationError as error:
                raise APIError(error)

            self.volumes.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.volumes)

    def __len__(self):
        """Return the length of the object."""
        return len(self.volumes)

    def __getitem__(self, index: int):
        """Return the result object at the passed index."""
        return self.volumes[index]
