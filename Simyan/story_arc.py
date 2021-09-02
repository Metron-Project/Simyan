from marshmallow import EXCLUDE, Schema, fields, post_load

from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class StoryArc:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class StoryArcSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    description = fields.Str(allow_none=True)
    # Ignoring Episodes
    # Ignoring First Episode
    first_issue = fields.Nested(IssueEntrySchema, data_key="first_appeared_in_issue")
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_isssue_appearances")
    issues = fields.Nested(GenericEntrySchema, many=True)
    # Ignoring Movies
    name = fields.Str()
    publisher = fields.Nested(GenericEntrySchema)
    site_url = fields.Url(data_key="site_detail_url")
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> StoryArc:
        return StoryArc(**data)
