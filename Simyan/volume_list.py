from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class VolumeResult:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class VolumeResultSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    description = fields.Str(allow_none=True)
    first_issue = fields.Nested(IssueEntrySchema)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_issues")
    last_issue = fields.Nested(IssueEntrySchema)
    name = fields.Str()
    publisher = fields.Nested(GenericEntrySchema)
    site_url = fields.Url(data_key="site_detail_url")
    start_year = fields.Str()
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> VolumeResult:
        return VolumeResult(**data)


class VolumeList:
    def __init__(self, response):
        self.volumes = []

        schema = VolumeResultSchema()
        for vol_dict in response:
            try:
                result = schema.load(vol_dict)
            except ValidationError as error:
                raise APIError(error)

            self.volumes.append(result)

    def __iter__(self):
        return iter(self.volumes)

    def __len__(self):
        return len(self.volumes)

    def __getitem__(self, index: int):
        return self.volumes[index]
