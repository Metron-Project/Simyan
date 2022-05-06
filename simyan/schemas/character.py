"""
The Character module.

This module provides the following classes:

- Character
- CharacterResult
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional

from dataclasses_json import Undefined, config, dataclass_json
from marshmallow import fields

from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Character:
    """The Character object contains information for a character."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the ComicVine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Character was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Character was updated on Comicvine.
    description: str  #: Long description of the Character.
    first_issue: IssueEntry = field(
        metadata=config(field_name="first_appeared_in_issue")
    )  #: First issue the Character appeared in.
    gender: int  #: Character gender.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in ComicVine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Character.
    name: str  #: Real name or public identity of Character.
    origin: GenericEntry  #: The type of Character.
    publisher: GenericEntry  #: The publisher of the Character.
    real_name: str  #: Name of the Character.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the ComicVine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Character has used, separated by ``\n``.
    creators: List[GenericEntry] = field(
        default_factory=list
    )  #: List of creators which worked on the Character.
    date_of_birth: Optional[date] = field(
        default=None,
        metadata=config(
            field_name="birth",
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
            mm_field=fields.Date(format="iso"),
        ),
    )  #: Date when the Character was born.
    deaths: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="issues_died_in")
    )  #: List of times when the Character has died.
    enemies: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="character_enemies")
    )  #: List of enemies the Character has.
    enemy_teams: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="team_enemies")
    )  #: List of enemy teams the Character has.
    friendly_teams: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="team_friends")
    )  #: List of friendly teams the Character has.
    friends: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="character_friends")
    )  #: List of friends the Character has.
    issue_count: Optional[int] = field(
        default=None, metadata=config(field_name="count_of_issue_appearances")
    )  #: Number of issues the Character appears in.
    issues: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="issue_credits")
    )  #: List of issues the Character appears in.
    powers: List[GenericEntry] = field(default_factory=list)  #: List of powers the Character has.
    story_arcs: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="story_arc_credits")
    )  #: List of story arcs the Character appears in.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Character.
    teams: List[GenericEntry] = field(
        default_factory=list
    )  #: List of teams the Character appears in.
    volumes: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="volume_credits")
    )  #: List of volumes the Character appears in.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CharacterResult:
    """The CharacterResult object contains information for a character."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the ComicVine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Character was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Character was updated on Comicvine.
    description: str  #: Long description of the Character.
    first_issue: IssueEntry = field(
        metadata=config(field_name="first_appeared_in_issue")
    )  #: First issue the Character appeared in.
    gender: int  #: Character gender.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in ComicVine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Character.
    name: str  #: Real name or public identity of Character.
    origin: GenericEntry  #: The type of Character.
    publisher: GenericEntry  #: The publisher of the Character.
    real_name: str  #: Name of the Character.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the ComicVine Website.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Character has used, separated by ``\n``.
    date_of_birth: Optional[date] = field(
        default=None,
        metadata=config(
            field_name="birth",
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
            mm_field=fields.Date(format="iso"),
        ),
    )  #: Date when the Character was born.
    issue_count: Optional[int] = field(
        default=None, metadata=config(field_name="count_of_issue_appearances")
    )  #: Number of issues the Character appears in.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Character.
