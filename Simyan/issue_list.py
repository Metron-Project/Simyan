from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema


class IssueResult:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueResultSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    cover_date = fields.Date(format="%Y-%m-%d")
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    description = fields.Str()
    has_staff_review = fields.Bool()
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    name = fields.Str(allow_none=True)
    number = fields.Str(data_key="issue_number")
    site_url = fields.Url(data_key="site_detail_url")
    store_date = fields.Date(format="%Y-%m-%d", allow_none=True)
    summary = fields.Str(data_key="deck", allow_none=True)
    volume = fields.Nested(GenericEntrySchema)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> IssueResult:
        return IssueResult(**data)


class IssueList:
    def __init__(self, response):
        self.issues = []

        schema = IssueResultSchema()
        for iss_dict in response:
            try:
                result = schema.load(iss_dict)
            except ValidationError as error:
                raise APIError(error)

            self.issues.append(result)

    def __iter__(self):
        return iter(self.issues)

    def __len__(self):
        return len(self.issues)

    def __getitem__(self, index: int):
        return self.issues[index]
