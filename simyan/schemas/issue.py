"""
The Issue module.

This module provides the following classes:

- Issue
- IssueResult
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional

from dataclasses_json import Undefined, config, dataclass_json
from marshmallow import fields

from simyan.schemas.generic_entries import CreatorEntry, GenericEntry, ImageEntry


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Issue:
    """The Issue object contains information for an issue."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Issue was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Issue was updated on Comicvine.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Issue.
    number: str = field(metadata=config(field_name="issue_number"))  #: The Issue number.
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    volume: GenericEntry  #: The volume the Issue is in.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Issue has used, separated by ``\n``.
    cover_date: Optional[date] = field(
        default=None,
        metadata=config(
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
        ),
    )  #: Date on the cover of the Issue.
    description: Optional[str] = field(default=None)  #: Long description of the Issue.
    first_appearance_characters: Optional[List[GenericEntry]] = field(
        default=None
    )  #: List of characters who first appear in the Issue.
    first_appearance_concepts: Optional[List[GenericEntry]] = field(
        default=None
    )  #: List of concepts which first appear in the Issue.
    first_appearance_locations: Optional[List[GenericEntry]] = field(
        default=None
    )  #: List of locations which first appear in the Issue.
    first_appearance_objects: Optional[List[GenericEntry]] = field(
        default=None
    )  #: List of objects which first appear in the Issue.
    first_appearance_story_arcs: Optional[List[GenericEntry]] = field(
        default=None, metadata=config(field_name="first_appearance_storyarcs")
    )  #: List of story arcs which start in the Issue.
    first_appearance_teams: Optional[List[GenericEntry]] = field(
        default=None
    )  #: List of teams which first appear in the Issue.
    name: Optional[str] = field(default=None)  #: Name/Title of the Issue.
    store_date: Optional[date] = field(
        default=None,
        metadata=config(
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
        ),
    )  #: Date the Issue went on sale on stores.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Issue.
    characters: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="character_credits")
    )  #: List of Characters in the Issue.
    concepts: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="concept_credits")
    )  #: List of Concepts in the Issue.
    creators: List[CreatorEntry] = field(
        default_factory=list, metadata=config(field_name="person_credits")
    )  #: List of Creators in the Issue.
    deaths: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="character_died_in")
    )  #: List of characters who died in the Issue.
    locations: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="location_credits")
    )  #: List of Locations in the Issue.
    objects: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="object_credits")
    )  #: List of Objects in the Issue.
    story_arcs: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="story_arc_credits")
    )  #: List of Story Arcs in the Issue.
    teams: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="team_credits")
    )  #: List of Teams in the Issue.
    teams_disbanded: List[GenericEntry] = field(
        default_factory=list, metadata=config(field_name="team_disbanded_in")
    )  #: List of Teams Disbanded in the Issue.


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class IssueResult:
    """The IssueResult object contains information for a issue."""

    api_url: str = field(metadata=config(field_name="api_detail_url"))  #: Url to the Comicvine API.
    date_added: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Issue was added to Comicvine.
    date_last_updated: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )  #: Date and time when the Issue was updated on Comicvine.
    id_: int = field(metadata=config(field_name="id"))  #: Identifier used in Comicvine.
    image: ImageEntry  #: Different sized images, posters and thumbnails for the Issue.
    number: str = field(metadata=config(field_name="issue_number"))
    site_url: str = field(
        metadata=config(field_name="site_detail_url")
    )  #: Url to the Comicvine Website.
    volume: GenericEntry  #: The volume the Issue is in.
    aliases: Optional[str] = field(
        default=None
    )  #: List of names the Issue has used, separated by ``\n``.
    cover_date: Optional[date] = field(
        default=None,
        metadata=config(
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
        ),
    )  #: Date on the cover of the Issue.
    description: Optional[str] = field(default=None)  #: Long description of the Issue.
    name: Optional[str] = field(default=None)  #: Name/Title of the Issue.
    store_date: Optional[date] = field(
        default=None,
        metadata=config(
            encoder=lambda x: x.isoformat() if x else None,
            decoder=lambda x: date.fromisoformat(x) if x else None,
        ),
    )  #: Date the Issue went on sale on stores.
    summary: Optional[str] = field(
        default=None, metadata=config(field_name="deck")
    )  #: Short description of the Issue.
