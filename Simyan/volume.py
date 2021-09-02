from marshmallow import EXCLUDE, Schema, fields, post_load

from Simyan.generic_entries import CountEntrySchema, GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class Volume:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class VolumeSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    characters = fields.Nested(CountEntrySchema, many=True)
    concepts = fields.Nested(CountEntrySchema, many=True)
    creators = fields.Nested(CountEntrySchema, data_key="people", many=True)
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    description = fields.Str(allow_none=True)
    first_issue = fields.Nested(IssueEntrySchema)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_issues")
    issues = fields.Nested(IssueEntrySchema, many=True)
    last_issue = fields.Nested(IssueEntrySchema)
    locations = fields.Nested(CountEntrySchema, many=True)
    name = fields.Str()
    objects = fields.Nested(CountEntrySchema, many=True)
    publisher = fields.Nested(GenericEntrySchema)
    site_url = fields.Url(data_key="site_detail_url")
    start_year = fields.Str()
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> Volume:
        return Volume(**data)
