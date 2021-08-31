from marshmallow import INCLUDE, Schema, fields, post_load


class PublisherEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class PublisherEntrySchema(Schema):
    api_url = fields.Url(data_key="api_detail_url")
    id = fields.Int()
    name = fields.Str()

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> PublisherEntry:
        return PublisherEntry(**data)
