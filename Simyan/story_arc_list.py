from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load

from Simyan.exceptions import APIError
from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema, IssueEntrySchema


class StoryArcResult:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class StoryArcResultSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    description = fields.Str(allow_none=True)
    # Ignoring First Episode
    first_issue = fields.Nested(IssueEntrySchema, data_key="first_appeared_in_issue")
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_isssue_appearances")
    name = fields.Str()
    publisher = fields.Nested(GenericEntrySchema)
    site_url = fields.Url(data_key="site_detail_url")
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> StoryArcResult:
        return StoryArcResult(**data)


class StoryArcList:
    def __init__(self, response):
        self.story_arcs = []

        schema = StoryArcResultSchema()
        for pub_dict in response:
            try:
                result = schema.load(pub_dict)
            except ValidationError as error:
                raise APIError(error)

            self.story_arcs.append(result)

    def __iter__(self):
        return iter(self.story_arcs)

    def __len__(self):
        return len(self.story_arcs)

    def __getitem__(self, index: int):
        return self.story_arcs[index]
