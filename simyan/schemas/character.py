"""The Character module.

This module provides the following classes:

- Character
- CharacterEntry
"""

from __future__ import annotations

__all__ = ["Character", "CharacterEntry"]
from datetime import date, datetime
from typing import Any

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

    aliases: str | None = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    date_of_birth: date | None = Field(alias="birth", default=None)
    description: str | None = None
    first_issue: IssueEntry | None = Field(alias="first_appeared_in_issue", default=None)
    gender: int
    id: int
    image: Image
    issue_count: int = Field(alias="count_of_issue_appearances")
    name: str
    origin: GenericEntry | None = None
    publisher: GenericEntry | None = None
    real_name: str | None = None
    site_url: str = Field(alias="site_detail_url")
    summary: str | None = Field(alias="deck", default=None)

    def __init__(self, **data: Any):
        if data.get("birth"):
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

    creators: list[GenericEntry] = Field(default_factory=list)
    deaths: list[GenericEntry] = Field(alias="issues_died_in", default_factory=list)
    enemies: list[GenericEntry] = Field(alias="character_enemies", default_factory=list)
    enemy_teams: list[GenericEntry] = Field(alias="team_enemies", default_factory=list)
    friendly_teams: list[GenericEntry] = Field(alias="team_friends", default_factory=list)
    friends: list[GenericEntry] = Field(alias="character_friends", default_factory=list)
    issues: list[GenericEntry] = Field(alias="issue_credits", default_factory=list)
    powers: list[GenericEntry] = Field(default_factory=list)
    story_arcs: list[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    teams: list[GenericEntry] = Field(default_factory=list)
    volumes: list[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class CharacterEntry(BaseCharacter):
    """Contains all the fields available when viewing a list of Characters."""
