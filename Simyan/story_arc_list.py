"""
Story Arc List module.

This module provides the following classes:

- StoryArcResult
- StoryArcResultSchema
- StoryArcList
"""
from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class StoryArcResult:
    """
    The StoryArcResult object contains information for story arcs.

    :param `**kwargs`: The keyword arguments is used for setting data from Comic Vine.
    """

    def __init__(self, **kwargs):
        """Intialize a new StoryArcResult."""
        for k, v in kwargs.items():
            setattr(self, k, v)


class StoryArcResultSchema(Schema):
    """Schema for the StoryArcResult API."""

    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    description = fields.Str(allow_none=True)
    # Ignoring First Episode
    first_issue = fields.Nested(IssueEntrySchema, data_key="first_appeared_in_issue")
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_isssue_appearances")
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
    def make_object(self, data, **kwargs) -> StoryArcResult:
        """
        Make the StoryArcResult object.

        :param data: Data from the Comic Vine response.

        :returns: :class:`StoryArcResult` object
        :rtype: StoryArcResult
        """
        return StoryArcResult(**data)


class StoryArcList:
    """The StoryArcsList object contains a list of `StoryArcResult` objects."""

    def __init__(self, response):
        """Initialize a new StoryArcList."""
        self.story_arcs = []

        schema = StoryArcResultSchema()
        for pub_dict in response:
            try:
                result = schema.load(pub_dict)
            except ValidationError as error:
                raise APIError(error)

            self.story_arcs.append(result)

    def __iter__(self):
        """Return an iterator object."""
        return iter(self.story_arcs)

    def __len__(self):
        """Return the length of the object."""
        return len(self.story_arcs)

    def __getitem__(self, index: int):
        """Return the object of a at index."""
        return self.story_arcs[index]
