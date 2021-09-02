from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import ImageEntrySchema


class PublisherResult:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class PublisherResultSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
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
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> PublisherResult:
        return PublisherResult(**data)


class PublisherList:
    def __init__(self, response):
        self.publishers = []

        schema = PublisherResultSchema()
        for pub_dict in response:
            try:
                result = schema.load(pub_dict)
            except ValidationError as error:
                raise APIError(error)

            self.publishers.append(result)

    def __iter__(self):
        return iter(self.publishers)

    def __len__(self):
        return len(self.publishers)

    def __getitem__(self, index: int):
        return self.publishers[index]
