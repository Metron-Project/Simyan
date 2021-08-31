from marshmallow import INCLUDE, Schema, fields, post_load


class TeamEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TeamEntrySchema(Schema):
    api_url = fields.Url(data_key="api_detail_url")
    id = fields.Int()
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> TeamEntry:
        return TeamEntry(**data)
