from marshmallow import INCLUDE, Schema, fields, post_load


class ImageEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ImageEntrySchema(Schema):
    icon = fields.Url(data_key="icon_url")
    medium = fields.Url(data_key="medium_url")
    screen = fields.Url(data_key="screen_url")
    screen_large = fields.Url(data_key="screen_large_url")
    small = fields.Url(data_key="small_url")
    super = fields.Url(data_key="super_url")
    thumb = fields.Url(data_key="thumb_url")
    tiny = fields.Url(data_key="tiny_url")
    original = fields.Url(data_key="original_url")
    tags = fields.Str(data_key="image_tags")

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> ImageEntry:
        return ImageEntry(**data)
