from marshmallow import Schema, fields, post_load, INCLUDE, ValidationError

from Simyan.exceptions import APIError
from Simyan import image
from Simyan.issue_entry import IssueEntrySchema
from Simyan.publisher_entry import PublisherEntrySchema


class StoryArc:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class StoryArcSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key='api_detail_url')
    issue_count = fields.Int(data_key='count_of_issue_appearances')
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    summary = fields.Str(data_key='deck', allow_none=True)
    description = fields.Str(allow_none=True)
    # Ignoring Episodes
    # Ignoring First Episode
    first_issue = fields.Nested(IssueEntrySchema, data_key='first_appeared_in_issue')
    id = fields.Int()
    image = fields.Nested(image.ImageEntrySchema)
    issues = fields.Nested(IssueEntrySchema, many=True)
    # Ignoring Movies
    name = fields.Str()
    publisher = fields.Nested(PublisherEntrySchema)
    site_url = fields.Url(data_key='site_detail_url')

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> StoryArc:
        return StoryArc(**data)


class StoryArcList:
    def __init__(self, response):
        self.story_arcs = []

        schema = StoryArcSchema()
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
