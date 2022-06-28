from enum import Enum
from typing import List

from simyan.schemas.character import Character
from simyan.schemas.creator import Creator
from simyan.schemas.issue import Issue
from simyan.schemas.volume import Volume


class ResourceType(Enum):
    CHARACTER = ["character", List[Character]]
    # CONCEPT = ["concept", List[Concept]] # TODO: Add Concept endpoint
    # LOCATION = ["location", List[Location]] # TODO: Add Location endpoint
    ISSUE = ["issue", List[Issue]]
    VOLUME = ["volume", List[Volume]]
    CREATOR = ["person", List[Creator]]
    # TEAM = ["team", List[Team]] # TODO: Add Team endpoint
