from marshmallow import INCLUDE, Schema, ValidationError, fields, post_load

from Simyan import character, image
from Simyan.exceptions import APIError
from Simyan.issue_entry import IssueEntrySchema
from Simyan.story_arc_entry import StoryArcEntrySchema
from Simyan.volume_entry import VolumeEntrySchema


class Creator:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    birth = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    issue_count = fields.Int(data_key="count_of_issue_appearances", allow_none=True)
    country = fields.Str()
    created_characters = fields.Nested(character.CharacterEntrySchema, many=True)
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    death = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    summary = fields.Str(data_key="deck", allow_none=True)
    description = fields.Str()
    email = fields.Str(allow_none=True)
    gender = fields.Int()
    hometown = fields.Str()
    id = fields.Int()
    image = fields.Nested(image.ImageEntrySchema)
    issues = fields.Nested(IssueEntrySchema, many=True)
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    story_arcs = fields.Nested(StoryArcEntrySchema, many=True)
    volumes = fields.Nested(VolumeEntrySchema, many=True)
    website = fields.Str()

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> Creator:
        return Creator(**data)


class CreatorList:
    def __init__(self, response):
        self.creators = []

        schema = CreatorSchema()
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
