from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import ImageEntrySchema


class CreatorResult:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorResultSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    country = fields.Str()
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_of_birth = fields.DateTime(format="%Y-%m-%d %H:%M:%S", data_key="birth", allow_none=True)
    date_of_death = fields.DateTime(format="%Y-%m-%d %H:%M:%S", data_key="death", allow_none=True)
    description = fields.Str()
    email = fields.Str(allow_none=True)
    gender = fields.Int()
    hometown = fields.Str(allow_none=True)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_isssue_appearances", allow_none=True)
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    summary = fields.Str(data_key="deck", allow_none=True)
    website = fields.Str(allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> CreatorResult:
        return CreatorResult(**data)


class CreatorList:
    def __init__(self, response):
        self.creators = []

        schema = CreatorResultSchema()
        for iss_dict in response:
            try:
                result = schema.load(iss_dict)
            except ValidationError as error:
                raise APIError(error)

            self.creators.append(result)

    def __iter__(self):
        return iter(self.creators)

    def __len__(self):
        return len(self.creators)

    def __getitem__(self, index: int):
        return self.creators[index]
