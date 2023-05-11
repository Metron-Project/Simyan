"""
The Issue module.

This module provides the following classes:

- Issue
- IssueEntry
"""
__all__ = ["Issue", "IssueEntry"]
import re
from datetime import date, datetime
from typing import Any, List, Optional

from pydantic import Field, validator

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import (
    AlternativeImageEntry,
    CreatorEntry,
    GenericEntry,
    ImageEntry,
)


class BaseIssue(BaseModel):
    r"""
    Contains fields for all Issues.

    Attributes:
        aliases: List of names used by the Issue, separated by `~\r\n`.
        alternative_images: List of different images associated with the Issue.
        api_url: Url to the resource in the Comicvine API.
        cover_date: Date on the cover of the Issue.
        date_added: Date and time when the Issue was added.
        date_last_updated: Date and time when the Issue was last updated.
        description: Long description of the Issue.
        issue_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Issue.
        name: Name/Title of the Issue.
        number: The Issue number.
        site_url: Url to the resource in Comicvine.
        store_date: Date the Issue went on sale on stores.
        summary: Short description of the Issue.
        volume: The volume the Issue is in.
    """

    aliases: Optional[str] = None
    alternative_images: List[AlternativeImageEntry] = Field(
        alias="associated_images",
        default_factory=list,
    )
    api_url: str = Field(alias="api_detail_url")
    cover_date: Optional[date] = None
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    issue_id: int = Field(alias="id")
    image: ImageEntry
    name: Optional[str] = None
    number: Optional[str] = Field(alias="issue_number", default=None)
    site_url: str = Field(alias="site_detail_url")
    store_date: Optional[date] = None
    summary: Optional[str] = Field(alias="deck", default=None)
    volume: GenericEntry

    @validator("store_date", "cover_date", pre=True)
    def validate_date_fields(cls, v: str) -> Optional[date]:
        """
        Convert date fields to date or None.

        Args:
            v: String value of the date fields in isoformat

        Returns:
            date value of field or None
        """
        if v and isinstance(v, str):
            try:
                return date.fromisoformat(v)
            except ValueError:
                return None
        return None

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Issue has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []


class Issue(BaseIssue):
    r"""
    Extends BaseIssue by including all the list references of an issue.

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

    characters: List[GenericEntry] = Field(alias="character_credits", default_factory=list)
    concepts: List[GenericEntry] = Field(alias="concept_credits", default_factory=list)
    creators: List[CreatorEntry] = Field(alias="person_credits", default_factory=list)
    deaths: List[GenericEntry] = Field(alias="character_died_in", default_factory=list)
    first_appearance_characters: List[GenericEntry] = Field(default_factory=list)
    first_appearance_concepts: List[GenericEntry] = Field(default_factory=list)
    first_appearance_locations: List[GenericEntry] = Field(default_factory=list)
    first_appearance_objects: List[GenericEntry] = Field(default_factory=list)
    first_appearance_story_arcs: List[GenericEntry] = Field(
        alias="first_appearance_storyarcs",
        default_factory=list,
    )
    first_appearance_teams: List[GenericEntry] = Field(default_factory=list)
    locations: List[GenericEntry] = Field(alias="location_credits", default_factory=list)
    objects: List[GenericEntry] = Field(alias="object_credits", default_factory=list)
    story_arcs: List[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    teams: List[GenericEntry] = Field(alias="team_credits", default_factory=list)
    teams_disbanded: List[GenericEntry] = Field(alias="team_disbanded_in", default_factory=list)

    def __init__(self, **data: Any):
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


class IssueEntry(BaseIssue):
    """Contains all the fields available when viewing a list of Issues."""
