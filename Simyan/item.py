from marshmallow import INCLUDE, Schema, fields, post_load


class ItemEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ItemEntrySchema(Schema):
    api_url = fields.Url(data_key="api_detail_url")
    id = fields.Int()
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    count = fields.Str()

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_Item(self, data, **kwargs) -> ItemEntry:
        return ItemEntry(**data)
