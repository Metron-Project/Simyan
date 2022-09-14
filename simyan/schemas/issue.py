"""
The Issue module.

This module provides the following classes:

- Issue
- IssueEntry
"""
__all__ = ["Issue", "IssueEntry"]
import re
from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import (
    AlternativeImageEntry,
    CreatorEntry,
    GenericEntry,
    ImageEntry,
)


class Issue(BaseModel):
    r"""
    The Issue object contains information for an issue.

    Attributes:
        aliases: List of names used by the Issue, separated by `~\r\n`.
        alternative_images: List of different images associated with the Issue.
        api_url: Url to the resource in the Comicvine API.
        characters: List of characters in the Issue.
        concepts: List of concepts in the Issue.
        cover_date: Date on the cover of the Issue.
        creators: List of creators in the Issue.
        date_added: Date and time when the Issue was added.
        date_last_updated: Date and time when the Issue was last updated.
        deaths: List of characters who died in the Issue.
        description: Long description of the Issue.
        first_appearance_characters: List of characters who first appear in the Issue.
        first_appearance_concepts: List of concepts which first appear in the Issue.
        first_appearance_locations: List of locations which first appear in the Issue.
        first_appearance_objects: List of objects which first appear in the Issue.
        first_appearance_story_arcs: List of story arcs which first appear in the Issue.
        first_appearance_teams: List of teams who first appear in the Issue.
        issue_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Issue.
        locations: List of locations in the Issue.
        name: Name/Title of the Issue.
        number: The Issue number
        objects: List of objects in the Issue.
        site_url: Url to the resource in Comicvine.
        store_date: Date the Issue went on sale on stores.
        story_arcs: List of story arcs in the Issue.
        summary: Short description of the Issue.
        teams: List of teams in the Issue.
        teams_disbanded: List of teams who disbanded in the Issue.
        volume: The volume the Issue is in.
    """

    aliases: Optional[str] = None
    alternative_images: List[AlternativeImageEntry] = Field(
        default_factory=list, alias="associated_images"
    )
    api_url: str = Field(alias="api_detail_url")
    characters: List[GenericEntry] = Field(default_factory=list, alias="character_credits")
    concepts: List[GenericEntry] = Field(default_factory=list, alias="concept_credits")
    cover_date: Optional[date] = None
    creators: List[CreatorEntry] = Field(default_factory=list, alias="person_credits")
    date_added: datetime
    date_last_updated: datetime
    deaths: List[GenericEntry] = Field(default_factory=list, alias="character_died_in")
    description: Optional[str] = None
    first_appearance_characters: List[GenericEntry] = Field(default_factory=list)
    first_appearance_concepts: List[GenericEntry] = Field(default_factory=list)
    first_appearance_locations: List[GenericEntry] = Field(default_factory=list)
    first_appearance_objects: List[GenericEntry] = Field(default_factory=list)
    first_appearance_story_arcs: List[GenericEntry] = Field(
        default_factory=list, alias="first_appearance_storyarcs"
    )
    first_appearance_teams: List[GenericEntry] = Field(default_factory=list)
    issue_id: int = Field(alias="id")
    image: ImageEntry
    locations: List[GenericEntry] = Field(default_factory=list, alias="location_credits")
    name: Optional[str] = None
    number: str = Field(alias="issue_number")
    objects: List[GenericEntry] = Field(default_factory=list, alias="object_credits")
    site_url: str = Field(alias="site_detail_url")
    store_date: Optional[date] = None
    story_arcs: List[GenericEntry] = Field(default_factory=list, alias="story_arc_credits")
    summary: Optional[str] = Field(default=None, alias="deck")
    teams: List[GenericEntry] = Field(default_factory=list, alias="team_credits")
    teams_disbanded: List[GenericEntry] = Field(default_factory=list, alias="team_disbanded_in")
    volume: GenericEntry

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
        r"""
        List of aliases the Issue has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []


class IssueEntry(BaseModel):
    r"""
    The IssueEntry object contains information for an issue.

    Attributes:
        aliases: List of names used by the IssueEntry, separated by `~\r\n`.
        alternative_images: List of different images associated with the IssueEntry.
        api_url: Url to the resource in the Comicvine API.
        cover_date: Date on the cover of the IssueEntry.
        date_added: Date and time when the IssueEntry was added.
        date_last_updated: Date and time when the IssueEntry was last updated.
        description: Long description of the IssueEntry.
        issue_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the IssueEntry.
        name: Name/Title of the IssueEntry.
        number: The IssueEntry number.
        site_url: Url to the resource in Comicvine.
        store_date: Date the IssueEntry went on sale on stores.
        summary: Short description of the IssueEntry.
        volume: The volume the IssueEntry is in.
    """

    aliases: Optional[str] = None
    alternative_images: List[AlternativeImageEntry] = Field(
        default_factory=list, alias="associated_images"
    )
    api_url: str = Field(alias="api_detail_url")
    cover_date: Optional[date] = None
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    issue_id: int = Field(alias="id")
    image: ImageEntry
    name: Optional[str] = None
    number: str = Field(alias="issue_number")
    site_url: str = Field(alias="site_detail_url")
    store_date: Optional[date] = None
    summary: Optional[str] = Field(default=None, alias="deck")
    volume: GenericEntry

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Issue has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []
