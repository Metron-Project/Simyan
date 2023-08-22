"""The Team module.

This module provides the following classes:

- Team
- TeamEntry
"""
__all__ = ["Team", "TeamEntry"]
from datetime import datetime
from typing import List, Optional

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

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: Optional[IssueEntry] = Field(alias="first_appeared_in_issue", default=None)
    id: int  # noqa: A003
    image: Image
    issue_count: int = Field(alias="count_of_isssue_appearances")
    member_count: int = Field(alias="count_of_team_members")
    name: str
    publisher: Optional[GenericEntry] = None
    site_url: str = Field(alias="site_detail_url")
    summary: Optional[str] = Field(alias="deck", default=None)


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

    enemies: List[GenericEntry] = Field(alias="character_enemies", default_factory=list)
    friends: List[GenericEntry] = Field(alias="character_friends", default_factory=list)
    issues: List[GenericEntry] = Field(alias="issue_credits", default_factory=list)
    issues_disbanded_in: List[GenericEntry] = Field(
        alias="disbanded_in_issues",
        default_factory=list,
    )
    members: List[GenericEntry] = Field(alias="characters", default_factory=list)
    story_arcs: List[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    volumes: List[GenericEntry] = Field(alias="volume_credits", default_factory=list)


class TeamEntry(BaseTeam):
    """Contains all the fields available when viewing a list of Teams."""
