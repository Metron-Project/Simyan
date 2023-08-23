"""The Character module.

This module provides the following classes:

- Character
- CharacterEntry
"""
__all__ = ["Character", "CharacterEntry"]
from datetime import date, datetime
from typing import Any, List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, Image, IssueEntry


class BaseCharacter(BaseModel):
    r"""Contains fields for all Characters.

    Attributes:
        aliases: List of names used by the Character, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Character was added.
        date_last_updated: Date and time when the Character was last updated.
        date_of_birth: Date when the Character was born.
        description: Long description of the Character.
        first_issue: First issue the Character appeared in.
        gender: Character gender.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Character.
        issue_count: Number of issues the Character appears in.
        name: Real name or public identity of Character.
        origin: The type of Character.
        publisher: The publisher of the Character.
        real_name: Name of the Character.
        site_url: Url to the resource in Comicvine.
        summary: Short description of the Character.
    """
    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    date_of_birth: Optional[date] = Field(alias="birth", default=None)
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = Field(alias="first_appeared_in_issue", default=None)
    gender: int
    id: int  # noqa: A003
    image: Image
    issue_count: int = Field(alias="count_of_issue_appearances")
    name: str
    origin: Optional[GenericEntry] = None
    publisher: Optional[GenericEntry] = None
    real_name: Optional[str] = None
    site_url: str = Field(alias="site_detail_url")
    summary: Optional[str] = Field(alias="deck", default=None)

    def __init__(self: "BaseCharacter", **data: Any):
        if "birth" in data and data["birth"]:
            data["birth"] = datetime.strptime(data["birth"], "%b %d, %Y").date()  # noqa: DTZ007
        super().__init__(**data)


class Character(BaseCharacter):
    r"""Extends BaseCharacter by including all the list references of a character.

    Attributes:
        creators: List of creators which worked on the Character.
        deaths: List of times when the Character has died.
        enemies: List of enemies the Character has.
        enemy_teams: List of enemy teams the Character has.
        friendly_teams: List of friendly teams the Character has.
        friends: List of friends the Character has.
        issues: List of issues the Character appears in.
        powers: List of powers the Character has.
        story_arcs: List of story arcs the Character appears in.
        teams: List of teams the Character appears in.
        volumes: List of volumes the Character appears in.
    """

    creators: List[GenericEntry] = Field(default_factory=list)
    deaths: List[GenericEntry] = Field(alias="issues_died_in", default_factory=list)
    enemies: List[GenericEntry] = Field(alias="character_enemies", default_factory=list)
    enemy_teams: List[GenericEntry] = Field(alias="team_enemies", default_factory=list)
    friendly_teams: List[GenericEntry] = Field(alias="team_friends", default_factory=list)
    friends: List[GenericEntry] = Field(alias="character_friends", default_factory=list)
    issues: List[GenericEntry] = Field(alias="issue_credits", default_factory=list)
    powers: List[GenericEntry] = Field(default_factory=list)
    story_arcs: List[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    teams: List[GenericEntry] = Field(default_factory=list)
    volumes: List[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class CharacterEntry(BaseCharacter):
    """Contains all the fields available when viewing a list of Characters."""
