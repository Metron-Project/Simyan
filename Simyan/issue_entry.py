from marshmallow import INCLUDE, Schema, fields, post_load


class IssueEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueEntrySchema(Schema):
    api_url = fields.Url(data_key="api_detail_url")
    id = fields.Int()
    name = fields.Str(allow_none=True)
    number = fields.Str(data_key="issue_number", allow_none=True)

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> IssueEntry:
        return IssueEntry(**data)
