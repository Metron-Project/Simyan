__all__ = [
    "CHARACTER",
    "CONCEPT",
    "CREATOR",
    "ISSUE",
    "ITEM",
    "LOCATION",
    "ORIGIN",
    "POWER",
    "PUBLISHER",
    "STORY_ARC",
    "TEAM",
    "VOLUME",
    "PluralT",
    "Resource",
    "SingularT",
]

from dataclasses import dataclass
from typing import Generic, TypeVar

from simyan.schemas import (
    BasicCharacter,
    BasicConcept,
    BasicCreator,
    BasicIssue,
    BasicItem,
    BasicLocation,
    BasicOrigin,
    BasicPower,
    BasicPublisher,
    BasicStoryArc,
    BasicTeam,
    BasicVolume,
    Character,
    Concept,
    Creator,
    Issue,
    Item,
    Location,
    Origin,
    Power,
    Publisher,
    StoryArc,
    Team,
    Volume,
)

SingularT = TypeVar("SingularT")
PluralT = TypeVar("PluralT")


@dataclass(frozen=True)
class Resource(Generic[SingularT, PluralT]):  # noqa: D101
    resource: int
    singular: str
    plural: str
    singular_type: type[SingularT]
    plural_type: type[PluralT]

    def singular_endpoint(self, id_: int) -> str:  # noqa: D102
        return f"/{self.singular}/{self.resource}-{id_}/"

    def plural_endpoint(self) -> str:  # noqa: D102
        return f"/{self.plural}/"


ISSUE = Resource(4000, "issue", "issues", Issue, BasicIssue)
CHARACTER = Resource(4005, "character", "characters", Character, BasicCharacter)
PUBLISHER = Resource(4010, "publisher", "publishers", Publisher, BasicPublisher)
CONCEPT = Resource(4015, "concept", "concepts", Concept, BasicConcept)
LOCATION = Resource(4020, "location", "locations", Location, BasicLocation)
ORIGIN = Resource(4030, "origin", "origins", Origin, BasicOrigin)
POWER = Resource(4035, "power", "powers", Power, BasicPower)
CREATOR = Resource(4040, "person", "people", Creator, BasicCreator)
STORY_ARC = Resource(4045, "story_arc", "story_arcs", StoryArc, BasicStoryArc)
VOLUME = Resource(4050, "volume", "volumes", Volume, BasicVolume)
ITEM = Resource(4055, "object", "objects", Item, BasicItem)
TEAM = Resource(4060, "team", "teams", Team, BasicTeam)
