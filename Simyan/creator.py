from marshmallow import EXCLUDE, Schema, fields, post_load
from marshmallow.decorators import pre_load

from Simyan.generic_entries import GenericEntrySchema, ImageEntrySchema


class Creator:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class CreatorSchema(Schema):
    aliases = fields.Str(allow_none=True)
    api_url = fields.Url(data_key="api_detail_url")
    country = fields.Str()
    created_characters = fields.Nested(GenericEntrySchema, many=True)
    date_added = fields.DateTime()
    date_last_updated = fields.DateTime()
    date_of_birth = fields.DateTime(data_key="birth", allow_none=True)
    date_of_death = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f", data_key="death", allow_none=True)
    description = fields.Str()
    email = fields.Str(allow_none=True)
    gender = fields.Int()
    hometown = fields.Str(allow_none=True)
    id = fields.Int()
    image = fields.Nested(ImageEntrySchema)
    issue_count = fields.Int(data_key="count_of_isssue_appearances", allow_none=True)
    issues = fields.Nested(GenericEntrySchema, many=True)
    name = fields.Str()
    site_url = fields.Url(data_key="site_detail_url")
    story_arcs = fields.Nested(GenericEntrySchema, data_key="story_arc_credits", many=True)
    summary = fields.Str(data_key="deck", allow_none=True)
    volumes = fields.Nested(GenericEntrySchema, data_key="volume_credits", many=True)
    website = fields.Str(allow_none=True)

    class Meta:
        unknown = EXCLUDE
        dateformat = "%Y-%m-%d %H:%M:%S"

    @pre_load
    def process_input(self, data, **kwargs):
        new_data = data

        if "death" in new_data and new_data["death"] is not None:
            new_data["death"] = new_data["death"]["date"]

        return new_data

    @post_load
    def make_object(self, data, **kwargs) -> Creator:
        return Creator(**data)
