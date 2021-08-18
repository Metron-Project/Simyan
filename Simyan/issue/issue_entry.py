from marshmallow import Schema, fields, post_load, INCLUDE


class IssueEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueEntrySchema(Schema):
    api_url = fields.Url(data_key='api_detail_url')
    id = fields.Int()
    name = fields.Str(allow_none=True)
    issue_number = fields.Str()

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> IssueEntry:
        return IssueEntry(**data)
