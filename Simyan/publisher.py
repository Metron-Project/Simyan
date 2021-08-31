from marshmallow import INCLUDE, Schema, ValidationError, fields, post_load

from Simyan import character, image, team
from Simyan.exceptions import APIError
from Simyan.story_arc_entry import StoryArcEntrySchema
from Simyan.volume_entry import VolumeEntrySchema


class Publisher:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class PublisherSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    characters = fields.Nested(character.CharacterEntrySchema, many=True)
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    summary = fields.Str(data_key="deck", allow_none=True)
    description = fields.Str(allow_none=True)
    id = fields.Int()
    image = fields.Nested(image.ImageEntrySchema)
    location_address = fields.Str(allow_none=True)
    location_city = fields.Str(allow_none=True)
    location_state = fields.Str(allow_none=True)
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    story_arcs = fields.Nested(StoryArcEntrySchema, many=True)
    teams = fields.Nested(team.TeamEntrySchema, many=True)
    volumes = fields.Nested(VolumeEntrySchema, many=True)

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> Publisher:
        return Publisher(**data)


class PublisherList:
    def __init__(self, response):
        self.publishers = []

        schema = PublisherSchema()
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
