from marshmallow import EXCLUDE, Schema, fields, post_load


class GenericEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class GenericEntrySchema(Schema):
    api_url = fields.Url(data_key="api_detail_url")
    id = fields.Int()
    name = fields.Str(allow_none=True)
    site_url = fields.Url(data_key="site_detail_url", allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> GenericEntry:
        return GenericEntry(**data)


class CountEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CountEntrySchema(GenericEntrySchema):
    count = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> CountEntry:
        return CountEntry(**data)


class IssueEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueEntrySchema(GenericEntrySchema):
    number = fields.Str(data_key="issue_number", allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> IssueEntry:
        return IssueEntry(**data)


class CreatorEntry:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorEntrySchema(GenericEntrySchema):
    roles = fields.Str(data_key="role")

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> CreatorEntry:
        return CreatorEntry(**data)


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
    tags = fields.Str(data_key="image_tags", allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> ImageEntry:
        return ImageEntry(**data)
