"""
The Character module.

This module provides the following classes:

- Character
"""
import re
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


class Character(BaseModel):
    """The Character object contains information for a character."""

    aliases: Optional[str] = Field(
        default=None
    )  #: List of names the Character has used, separated by ``\n``.
    api_url: str = Field(alias="api_detail_url")  #: Url to the ComicVine API.
    creators: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of creators which worked on the Character.
    date_added: datetime  #: Date and time when the Character was added to Comicvine.
    date_last_updated: datetime  #: Date and time when the Character was updated on Comicvine.
    date_of_birth: Optional[date] = Field(
        default=None, alias="birth"
    )  #: Date when the Character was born.
    deaths: List[GenericEntry] = Field(
        default_factory=list, alias="issues_died_in"
    )  #: List of times when the Character has died.
    description: Optional[str] = Field(default=None)  #: Long description of the Character.
    enemies: List[GenericEntry] = Field(
        default_factory=list, alias="character_enemies"
    )  #: List of enemies the Character has.
    enemy_teams: List[GenericEntry] = Field(
        default_factory=list, alias="team_enemies"
    )  #: List of enemy teams the Character has.
    first_issue: IssueEntry = Field(
        alias="first_appeared_in_issue"
    )  #: First issue the Character appeared in.
    friendly_teams: List[GenericEntry] = Field(
        default_factory=list, alias="team_friends"
    )  #: List of friendly teams the Character has.
    friends: List[GenericEntry] = Field(
        default_factory=list, alias="character_friends"
    )  #: List of friends the Character has.
    gender: int  #: Character gender.
    id_: int = Field(alias="id")  #: Identifier used in ComicVine.
    character_id: int = Field(alias="id")  #: Identifier used in ComicVine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Character.
    issue_count: Optional[int] = Field(
        default=None, alias="count_of_issue_appearances"
    )  #: Number of issues the Character appears in.
    issues: List[GenericEntry] = Field(
        default_factory=list, alias="issue_credits"
    )  #: List of issues the Character appears in.
    name: str  #: Real name or public identity of Character.
    origin: Optional[GenericEntry] = Field(default=None)  #: The type of Character.
    powers: List[GenericEntry] = Field(default_factory=list)  #: List of powers the Character has.
    publisher: GenericEntry  #: The publisher of the Character.
    real_name: Optional[str] = Field(default=None)  #: Name of the Character.
    site_url: str = Field(alias="site_detail_url")  #: Url to the ComicVine Website.
    story_arcs: List[GenericEntry] = Field(
        default_factory=list, alias="story_arc_credits"
    )  #: List of story arcs the Character appears in.
    summary: Optional[str] = Field(
        default=None, alias="deck"
    )  #: Short description of the Character.
    teams: List[GenericEntry] = Field(
        default_factory=list
    )  #: List of teams the Character appears in.
    volumes: List[GenericEntry] = Field(
        default_factory=list, alias="volume_credits"
    )  #: List of volumes the Character appears in.

    @property
    def alias_list(self) -> List[str]:
        """List of names the Character has used."""
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        extra = Extra.ignore
