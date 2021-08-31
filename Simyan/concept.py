from marshmallow import INCLUDE, Schema, fields, post_load


class ConceptEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ConceptEntrySchema(Schema):
    api_url = fields.Url(data_key="api_detail_url")
    id = fields.Int()
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    count = fields.Str()

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> ConceptEntry:
        return ConceptEntry(**data)
