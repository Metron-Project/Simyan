"""The Team module.

This module provides the following classes:

- Team
- TeamEntry
"""

from __future__ import annotations

__all__ = ["Team", "TeamEntry"]
from datetime import datetime

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, Image, IssueEntry


class BaseTeam(BaseModel):
    r"""Contains fields for all Teams.

    Attributes:
        aliases: List of names used by the Team, collected in a string.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Team was added.
        date_last_updated: Date and time when the Team was last updated.
        description: Long description of the Team.
        first_issue: First issue the Team appeared in.
        id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Team.
        issue_count: Number of issues the Team appears in.
        member_count: Number of members in the Team.
        name: Name/Title of the Team.
        publisher: The publisher of the Team.
        site_url: Url to the resource in Comicvine.
        summary: Short description of the Team.
    """

    aliases: str | None = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: str | None = None
    first_issue: IssueEntry | None = Field(alias="first_appeared_in_issue", default=None)
    id: int
    image: Image
    issue_count: int = Field(alias="count_of_isssue_appearances")
    member_count: int = Field(alias="count_of_team_members")
    name: str
    publisher: GenericEntry | None = None
    site_url: str = Field(alias="site_detail_url")
    summary: str | None = Field(alias="deck", default=None)


class Team(BaseTeam):
    r"""Extends BaseTeam by including all the list references of a team.

    Attributes:
        enemies: List of enemies of the Team.
        friends: List of friends of the Team.
        issues: List of issues the Team appears in.
        issues_disbanded_in: List of issues the Team disbanded in.
        members: List of members in the Team.
        story_arcs: List of story arcs the Team appears in.
        volumes: List of volumes the Team appears in.
    """

    enemies: list[GenericEntry] = Field(alias="character_enemies", default_factory=list)
    friends: list[GenericEntry] = Field(alias="character_friends", default_factory=list)
    issues: list[GenericEntry] = Field(alias="issue_credits", default_factory=list)
    issues_disbanded_in: list[GenericEntry] = Field(
        alias="disbanded_in_issues", default_factory=list
    )
    members: list[GenericEntry] = Field(alias="characters", default_factory=list)
    story_arcs: list[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    volumes: list[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class TeamEntry(BaseTeam):
    """Contains all the fields available when viewing a list of Teams."""
