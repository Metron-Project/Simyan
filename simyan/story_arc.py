"""
The StoryArc module.

This module provides the following classes:

- StoryArc
- StoryArcSchema
"""
from typing import Any, Dict

from marshmallow import EXCLUDE, Schema, fields, post_load

from simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class StoryArc:
    r"""
    The StoryArc object contains information for a story arc.

    Args:
        **kwargs: The keyword argument is used for setting data from ComicVine.

    Attributes:
        aliases (str): List of names the Story Arc has used, separated by ``\n``.
        api_url (str): Url to the ComicVine API.
        date_added (datetime): Date and time when the Story Arc was added to ComicVine.
        date_last_updated (datetime): Date and time when the Story Arc was updated on ComicVine.
        description (str, Optional): Long description of the Story Arc.
        first_issue (IssueEntry): First issue of the Story Arc.
        id (int): Identifier used in ComicVine.
        image (ImageEntry): Different sized images, posters and thumbnails for the Story Arc.
        issue_count (int): Number of issues in the Story Arc.
        issues (list of :obj: `GenericEntry`): List of issues in the Story Arc.
        name (str): Name/Title of the Story Arc.
        publisher (GenericEntry): The publisher of the Story Arc.
        site_url (str): Url to the ComicVine Website.
        summary (str, Optional): Short description of the Story Arc.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class StoryArcSchema(Schema):
    """Schema for the StoryArc API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    description = fields.Str(allow_none=True)
    first_issue = fields.Nested(IssueEntrySchema, data_key="first_appeared_in_issue")
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_isssue_appearances")
    issues = fields.Nested(GenericEntrySchema, many=True)
    name = fields.Str()
    publisher = fields.Nested(GenericEntrySchema)
    site_url = fields.Url(data_key="site_detail_url")
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        """Any unknown fields will be excluded."""

        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"
        datetimeformat = "%Y-%m-%d %H:%M:%S"

    @post_load
    def make_object(self, data: Dict[str, Any], **kwargs) -> StoryArc:
        """
        Make the StoryArc object.

        Args:
            data: Data from the ComicVine response.
            **kwargs:

        Returns:
            A StoryArc object
        """
        return StoryArc(**data)
