"""
The Team module.

This module provides the following classes:

- Team
- TeamEntry
"""
__all__ = ["Team", "TeamEntry"]
import re
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


class Team(BaseModel):
    r"""
    The Team object contains information for a team.

    Attributes:
        aliases: List of names used by the Team, separated by `~\r\n`.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the Team was added.
        date_last_updated: Date and time when the Team was last updated.
        description: Long description of the Team.
        enemies: List of enemies of the Team.
        first_issue: First issue the Team appeared in.
        friends: List of friends of the Team.
        image: Different sized images, posters and thumbnails for the Team.
        issue_count: Number of issues the Team appears in.
        issues: List of issues the Team appears in.
        issues_disbanded_in: List of issues the Team disbanded in.
        member_count: Number of members in the Team.
        members: List of members in the Team.
        name: Name/Title of the Team.
        publisher: The publisher of the Team.
        site_url: Url to the resource in Comicvine.
        story_arcs: List of story arcs the Team appears in.
        summary: Short description of the Team.
        team_id: Identifier used by Comicvine.
        volumes: List of volumes the Team appears in.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    enemies: List[GenericEntry] = Field(alias="character_enemies", default_factory=list)
    first_issue: IssueEntry = Field(alias="first_appeared_in_issue")
    friends: List[GenericEntry] = Field(alias="character_friends", default_factory=list)
    image: ImageEntry
    issue_count: int = Field(alias="count_of_isssue_appearances")
    issues: List[GenericEntry] = Field(alias="issue_credits", default_factory=list)
    issues_disbanded_in: List[GenericEntry] = Field(
        alias="disbanded_in_issues", default_factory=list
    )
    member_count: int = Field(alias="count_of_team_members")
    members: List[GenericEntry] = Field(alias="characters", default_factory=list)
    name: str
    publisher: GenericEntry
    site_url: str = Field(alias="site_detail_url")
    story_arcs: List[GenericEntry] = Field(alias="story_arc_credits", default_factory=list)
    summary: Optional[str] = Field(alias="deck", default=None)
    team_id: int = Field(alias="id")
    volumes: List[GenericEntry] = Field(alias="volume_credits", default_factory=list)

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Team has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []


class TeamEntry(BaseModel):
    r"""
    The TeamEntry object contains information for a team.

    Attributes:
        aliases: List of names used by the TeamEntry, separated by `~\r\n`.
        api_url: Url to the resource in the Comicvine API.
        date_added: Date and time when the TeamEntry was added.
        date_last_updated: Date and time when the TeamEntry was last updated.
        description: Long description of the TeamEntry.
        first_issue: First issue the TeamEntry appeared in.
        image: Different sized images, posters and thumbnails for the TeamEntry.
        issue_count: Number of issues the TeamEntry appears in.
        member_count: Number of members in the TeamEntry.
        name: Name/Title of the TeamEntry.
        publisher: The publisher of the TeamEntry.
        site_url: Url to the resource in Comicvine.
        summary: Short description of the TeamEntry.
        team_id: Identifier used by Comicvine.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    date_added: datetime
    date_last_updated: datetime
    description: Optional[str] = None
    first_issue: IssueEntry = Field(alias="first_appeared_in_issue")
    image: ImageEntry
    issue_count: int = Field(alias="count_of_isssue_appearances")
    member_count: int = Field(alias="count_of_team_members")
    name: str
    publisher: GenericEntry
    site_url: str = Field(alias="site_detail_url")
    summary: Optional[str] = Field(alias="deck", default=None)
    team_id: int = Field(alias="id")

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the TeamEntry has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []
