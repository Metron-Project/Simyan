from marshmallow import INCLUDE, Schema, ValidationError, fields, post_load

from Simyan import character, concept, image, item, location
from Simyan.creator_entry import CreatorEntrySchema
from Simyan.exceptions import APIError
from Simyan.issue_entry import IssueEntrySchema
from Simyan.publisher_entry import PublisherEntrySchema


class Volume:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class VolumeSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    characters = fields.Nested(character.CharacterEntrySchema, many=True)
    concepts = fields.Nested(concept.ConceptEntrySchema, many=True)
    creators = fields.Nested(CreatorEntrySchema, data_key="people", many=True)
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    description = fields.Str(allow_none=True)
    first_issue = fields.Nested(IssueEntrySchema)
    id = fields.Int()
    image = fields.Nested(image.ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_issues")
    issues = fields.Nested(IssueEntrySchema, many=True)
    last_issue = fields.Nested(IssueEntrySchema)
    locations = fields.Nested(location.LocationEntrySchema, many=True)
    name = fields.Str()
    objects = fields.Nested(item.ItemEntrySchema, many=True)
    publisher = fields.Nested(PublisherEntrySchema)
    site_url = fields.Url(data_key="site_detail_url")
    start_year = fields.Str()
    summary = fields.Str(data_key="deck", allow_none=True)

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> Volume:
        return Volume(**data)


class VolumeList:
    def __init__(self, response):
        self.volumes = []

        schema = VolumeSchema()
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
