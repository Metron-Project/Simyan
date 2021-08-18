from marshmallow import Schema, fields, post_load, INCLUDE, ValidationError

from Simyan import APIError, character, concept, image, location, item, people
from Simyan.issue.issue_entry import IssueEntrySchema
from Simyan.publisher.publisher_entry import PublisherEntrySchema


class Volume:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class VolumeSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key='api_detail_url')
    characters = fields.Nested(character.CharacterEntrySchema, many=True)
    concepts = fields.Nested(concept.ConceptEntrySchema, many=True)
    issue_count = fields.Int(data_key='count_of_issues')
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    summary = fields.Str(data_key='deck', allow_none=True)
    description = fields.Str(allow_none=True)
    first_issue = fields.Nested(IssueEntrySchema)
    id = fields.Int()
    image = fields.Nested(image.ImageEntrySchema)
    last_issue = fields.Nested(IssueEntrySchema)
    locations = fields.Nested(location.LocationEntrySchema, many=True)
    name = fields.Str()
    objects = fields.Nested(item.ItemEntrySchema, many=True)
    people = fields.Nested(people.PeopleEntrySchema, many=True)
    publisher = fields.Nested(PublisherEntrySchema)
    site_url = fields.Url(data_key='site_detail_url')
    start_year = fields.Str()

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> Volume:
        return Volume(**data)


class VolumeList:
    def __init__(self, response):
        self.volumes = []

        schema = VolumeSchema()
        for vol_dict in response["results"]:
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
