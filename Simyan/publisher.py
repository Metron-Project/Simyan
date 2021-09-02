from marshmallow import EXCLUDE, Schema, fields, post_load

from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema


class Publisher:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class PublisherSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    characters = fields.Nested(GenericEntrySchema, many=True)
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    description = fields.Str(allow_none=True)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    location_address = fields.Str(allow_none=True)
    location_city = fields.Str(allow_none=True)
    location_state = fields.Str(allow_none=True)
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    story_arcs = fields.Nested(GenericEntrySchema, data_key="story_arcs", many=True)
    summary = fields.Str(data_key="deck", allow_none=True)
    teams = fields.Nested(GenericEntrySchema, many=True)
    volumes = fields.Nested(GenericEntrySchema, many=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> Publisher:
        return Publisher(**data)
