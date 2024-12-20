"""The Issue module.

This module provides the following classes:
- BasicIssue
- Issue
"""

__all__ = ["BasicIssue", "Issue"]

from datetime import date, datetime
from typing import Optional, Union

from pydantic import Field, HttpUrl, field_validator

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import AssociatedImage, GenericCreator, GenericEntry, Images


class BasicIssue(BaseModel):
    r"""Contains fields for all Issues.

    Attributes:
        aliases: List of names used by the Issue, collected in a string.
        associated_images: List of different images associated with the Issue.
        api_url: Url to the resource in the Comicvine API.
        cover_date: Date on the cover of the Issue.
        date_added: Date and time when the Issue was added.
        date_last_updated: Date and time when the Issue was last updated.
        description: Long description of the Issue.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Issue.
        name: Name/Title of the Issue.
        number: The Issue number.
        site_url: Url to the resource in Comicvine.
        store_date: Date the Issue went on sale on stores.
        summary: Short description of the Issue.
        volume: The volume the Issue is in.
    """

    aliases: Optional[str] = None
    associated_images: list[AssociatedImage] = Field(default_factory=list)
    api_url: HttpUrl = Field(alias="api_detail_url")
    cover_date: Optional[date] = None
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    id: int
    image: Images
    name: Optional[str] = None
    number: Optional[str] = Field(alias="issue_number", default=None)
    site_url: HttpUrl = Field(alias="site_detail_url")
    store_date: Optional[date] = None
    summary: Optional[str] = Field(alias="deck", default=None)
    volume: GenericEntry


class Issue(BasicIssue):
    r"""Extends BasicIssue by including all the list references of an issue.

    Attributes:
        characters: List of characters in the Issue.
        concepts: List of concepts in the Issue.
        creators: List of creators in the Issue.
        deaths: List of characters who died in the Issue.
        first_appearance_characters: List of characters who first appear in the Issue.
        first_appearance_concepts: List of concepts which first appear in the Issue.
        first_appearance_locations: List of locations which first appear in the Issue.
        first_appearance_objects: List of objects which first appear in the Issue.
        first_appearance_story_arcs: List of story arcs which first appear in the Issue.
        first_appearance_teams: List of teams who first appear in the Issue.
        locations: List of locations in the Issue.
        objects: List of objects in the Issue.
        story_arcs: List of story arcs in the Issue.
        teams: List of teams in the Issue.
        teams_disbanded: List of teams who disbanded in the Issue.
    """

    characters: list[GenericEntry] = Field(alias="character_credits", default_factory=list)
    concepts: list[GenericEntry] = Field(alias="concept_credits", default_factory=list)
    creators: list[GenericCreator] = Field(alias="person_credits", default_factory=list)
    deaths: list[GenericEntry] = Field(alias="character_died_in", default_factory=list)
    first_appearance_characters: list[GenericEntry] = Field(default_factory=list)
    first_appearance_concepts: list[GenericEntry] = Field(default_factory=list)
    first_appearance_locations: list[GenericEntry] = Field(default_factory=list)
    first_appearance_objects: list[GenericEntry] = Field(default_factory=list)
    first_appearance_story_arcs: list[GenericEntry] = Field(
        alias="first_appearance_storyarcs", default_factory=list
    )
    first_appearance_teams: list[GenericEntry] = Field(default_factory=list)
    locations: list[GenericEntry] = Field(alias="location_credits", default_factory=list)
    objects: list[GenericEntry] = Field(alias="object_credits", default_factory=list)
    story_arcs: list[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    teams: list[GenericEntry] = Field(alias="team_credits", default_factory=list)
    teams_disbanded: list[GenericEntry] = Field(alias="team_disbanded_in", default_factory=list)

    @field_validator(
        "first_appearance_characters",
        "first_appearance_concepts",
        "first_appearance_locations",
        "first_appearance_objects",
        "first_appearance_story_arcs",
        "first_appearance_teams",
        mode="before",
    )
    def handle_blank_list(cls, value: Union[str, list, None]) -> list:
        return value or []
