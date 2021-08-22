from marshmallow import Schema, fields, post_load, INCLUDE, ValidationError

from Simyan import APIError, character, concept, image, location, item, people, arc, team
from Simyan.volume.volume_entry import VolumeEntrySchema


class Issue:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class IssueSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key='api_detail_url')
    character_credits = fields.Nested(character.CharacterEntrySchema, many=True)
    character_died_in = fields.Nested(character.CharacterEntrySchema, many=True)
    concept_credits = fields.Nested(concept.ConceptEntrySchema, many=True)
    cover_date = fields.Date(format="%Y-%m-%d")
    date_added = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    date_last_updated = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    summary = fields.Str(data_key='deck', allow_none=True)
    description = fields.Str()
    first_appearance_characters = fields.Str(allow_none=True)
    first_appearance_concepts = fields.Str(allow_none=True)
    first_appearance_locations = fields.Str(allow_none=True)
    first_appearance_objects = fields.Str(allow_none=True)
    first_appearance_storyarcs = fields.Str(allow_none=True)
    first_appearance_teams = fields.Str(allow_none=True)
    has_staff_review = fields.Bool()
    id = fields.Int()
    image = fields.Nested(image.ImageEntrySchema)
    issue_number = fields.Str()
    location_credits = fields.Nested(location.LocationEntrySchema, many=True)
    name = fields.Str()
    object_credits = fields.Nested(item.ItemEntrySchema, many=True)
    person_credits = fields.Nested(people.PeopleEntrySchema, many=True)
    site_url = fields.Url(data_key='site_detail_url')
    store_date = fields.Date(format="%Y-%m-%d")
    story_arc_credits = fields.Nested(arc.ArcEntrySchema, many=True)
    team_credits = fields.Nested(team.TeamEntrySchema, many=True)
    team_disbanded_in = fields.Nested(team.TeamEntrySchema, many=True)
    volume = fields.Nested(VolumeEntrySchema)

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_object(self, data, **kwargs) -> Issue:
        return Issue(**data)


class IssueList:
    def __init__(self, response):
        self.issues = []

        schema = IssueSchema()
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
