"""
The Issue module.

This module provides the following classes:

- Issue
"""
import re
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from simyan.schemas.generic_entries import CreatorEntry, GenericEntry, ImageEntry


class Issue(BaseModel):
    """The Issue object contains information for an issue."""

    aliases: Optional[str] = Field(
        default=None
    )  #: List of names the Issue has used, separated by ``\n``.
    api_url: str = Field(alias="api_detail_url")  #: Url to the Comicvine API.
    characters: List[GenericEntry] = Field(
        default_factory=list, alias="character_credits"
    )  #: List of Characters in the Issue.
    concepts: List[GenericEntry] = Field(
        default_factory=list, alias="concept_credits"
    )  #: List of Concepts in the Issue.
    cover_date: Optional[date] = Field(default=None)  #: Date on the cover of the Issue.
    creators: List[CreatorEntry] = Field(
        default_factory=list, alias="person_credits"
    )  #: List of Creators in the Issue.
    date_added: datetime  #: Date and time when the Issue was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Issue was updated on Comicvine.
    deaths: List[GenericEntry] = Field(
        default_factory=list, alias="character_died_in"
    )  #: List of characters who died in the Issue.
    description: Optional[str] = Field(default=None)  #: Long description of the Issue.
    first_appearance_characters: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of characters who first appear in the Issue.
    first_appearance_concepts: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of concepts which first appear in the Issue.
    first_appearance_locations: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of locations which first appear in the Issue.
    first_appearance_objects: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of objects which first appear in the Issue.
    first_appearance_story_arcs: List[GenericEntry] = Field(
        default_factory=list, alias="first_appearance_storyarcs"
    )  #: List of story arcs which start in the Issue.
    first_appearance_teams: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of teams which first appear in the Issue.
    id_: int = Field(alias="id")  #: Identifier used in Comicvine.
    issue_id: int = Field(alias="id")  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Issue.
    locations: List[GenericEntry] = Field(
        default_factory=list, alias="location_credits"
    )  #: List of Locations in the Issue.
    name: Optional[str] = Field(default=None)  #: Name/Title of the Issue.
    number: str = Field(alias="issue_number")  #: The Issue number.
    objects: List[GenericEntry] = Field(
        default_factory=list, alias="object_credits"
    )  #: List of Objects in the Issue.
    site_url: str = Field(alias="site_detail_url")  #: Url to the Comicvine Website.
    store_date: Optional[date] = Field(default=None)  #: Date the Issue went on sale on stores.
    story_arcs: List[GenericEntry] = Field(
        default_factory=list, alias="story_arc_credits"
    )  #: List of Story Arcs in the Issue.
    summary: Optional[str] = Field(default=None, alias="deck")  #: Short description of the Issue.
    teams: List[GenericEntry] = Field(
        default_factory=list, alias="team_credits"
    )  #: List of Teams in the Issue.
    teams_disbanded: List[GenericEntry] = Field(
        default_factory=list, alias="team_disbanded_in"
    )  #: List of Teams Disbanded in the Issue.
    volume: GenericEntry  #: The volume the Issue is in.

    def __init__(self, **data):
        if "first_appearance_characters" in data and not data["first_appearance_characters"]:
            data["first_appearance_characters"] = []
        if "first_appearance_concepts" in data and not data["first_appearance_concepts"]:
            data["first_appearance_concepts"] = []
        if "first_appearance_locations" in data and not data["first_appearance_locations"]:
            data["first_appearance_locations"] = []
        if "first_appearance_objects" in data and not data["first_appearance_objects"]:
            data["first_appearance_objects"] = []
        if "first_appearance_storyarcs" in data and not data["first_appearance_storyarcs"]:
            data["first_appearance_storyarcs"] = []
        if "first_appearance_teams" in data and not data["first_appearance_teams"]:
            data["first_appearance_teams"] = []
        super().__init__(**data)

    @property
    def alias_list(self) -> List[str]:
        """List of names the Issue has used."""
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.ignore
