"""
The Comicvine module.

This module provides the following classes:

- ComicvineResource
- Comicvine
"""
__all__ = ["ComicvineResource", "Comicvine"]
import platform
import re
from enum import Enum
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from urllib.parse import urlencode

from pydantic import ValidationError, parse_obj_as
from ratelimit import limits, sleep_and_retry
from requests import get
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout

from simyan import __version__
from simyan.exceptions import AuthenticationError, CacheError, ServiceError
from simyan.schemas.character import Character, CharacterEntry
from simyan.schemas.concept import Concept, ConceptEntry
from simyan.schemas.creator import Creator, CreatorEntry
from simyan.schemas.issue import Issue, IssueEntry
from simyan.schemas.item import Item, ItemEntry
from simyan.schemas.location import Location, LocationEntry
from simyan.schemas.origin import Origin, OriginEntry
from simyan.schemas.power import Power, PowerEntry
from simyan.schemas.publisher import Publisher, PublisherEntry
from simyan.schemas.story_arc import StoryArc, StoryArcEntry
from simyan.schemas.team import Team, TeamEntry
from simyan.schemas.volume import Volume, VolumeEntry
from simyan.sqlite_cache import SQLiteCache

MINUTE = 60
T = TypeVar("T")


class ComicvineResource(Enum):
    """Enum class for Comicvine Resources."""

    PUBLISHER = (4010, "publisher", List[PublisherEntry])
    """Details for the Publisher resource on Comicvine."""
    VOLUME = (4050, "volume", List[VolumeEntry])
    """Details for the Volume resource on Comicvine."""
    ISSUE = (4000, "issue", List[IssueEntry])
    """Details for the Issue resource on Comicvine."""
    STORY_ARC = (4045, "story_arc", List[StoryArcEntry])
    """Details for the Story Arc resource on Comicvine."""
    CREATOR = (4040, "person", List[CreatorEntry])
    """Details for the Creator resource on Comicvine."""
    CHARACTER = (4005, "character", List[CharacterEntry])
    """Details for the Character resource on Comicvine."""
    TEAM = (4060, "team", List[TeamEntry])
    """Details for the Team resource on Comicvine."""
    LOCATION = (4020, "location", List[LocationEntry])
    """Details for the Location resource on Comicvine."""
    CONCEPT = (4015, "concept", List[ConceptEntry])
    """Details for the Concept resource on Comicvine."""
    POWER = (4035, "power", List[PowerEntry])
    """Details for the Power resource on Comicvine."""
    ORIGIN = (4030, "origin", List[OriginEntry])
    """Details for the Origin resource on Comicvine."""
    ITEM = (4055, "object", List[ItemEntry])
    """Details for the Item resource on Comicvine."""

    @property
    def resource_id(self) -> int:
        """Start of id used by Comicvine to create unique ids."""
        return self.value[0]

    @property
    def search_resource(self) -> str:
        """Resource string for filtering searches."""
        return self.value[1]

    @property
    def search_response(self) -> Type[T]:
        """Response type for resource when using a search endpoint."""
        return self.value[2]


class Comicvine:
    """
    Comicvine to request Comicvine API endpoints.

    Args:
        api_key: User's API key to access the Comicvine API.
        timeout: Set how long requests will wait for a response (in seconds).
        cache: SQLiteCache to use if set.

    Attributes:
        headers (Dict[str, str]): Header used when requesting from Comicvine API.
        api_key (str): User's API key to access the Comicvine API.
        timeout (int): How long requests will wait for a response (in seconds).
        cache (Optional[SQLiteCache]): SQLiteCache to use if set.
    """

    API_URL = "https://comicvine.gamespot.com/api"

    def __init__(self, api_key: str, timeout: int = 30, cache: Optional[SQLiteCache] = None):
        self.headers = {
            "Accept": "application/json",
            "User-Agent": f"Simyan/{__version__}/{platform.system()}: {platform.release()}",
        }
        self.api_key = api_key
        self.timeout = timeout
        self.cache = cache

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _perform_get_request(self, url: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Make GET request to Comicvine API endpoint.

        Args:
            url: The url to request information from.
            params: Parameters to add to the request.

        Returns:
            Json response from the Comicvine API.

        Raises:
            ServiceError: If there is an issue with the request or response from the Comicvine API.
        """
        if params is None:
            params = {}

        try:
            response = get(url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except ConnectionError as err:
            raise ServiceError(f"Unable to connect to `{url}`") from err
        except HTTPError as err:
            if err.response.status_code == 401:
                raise AuthenticationError("Invalid API Key") from err
            if err.response.status_code == 404:
                raise ServiceError("Unknown endpoint") from err
            if err.response.status_code == 502:
                raise ServiceError("Service error, retry again in 30s") from err
            raise ServiceError(err.response.json()["error"]) from err
        except JSONDecodeError as err:
            raise ServiceError(f"Unable to parse response from `{url}` as Json") from err
        except ReadTimeout as err:
            raise ServiceError("Service took too long to respond") from err

    def _get_request(
        self,
        endpoint: str,
        params: Dict[str, str] = None,
        skip_cache: bool = False,
    ) -> Dict[str, Any]:
        """
        Check cache or make GET request to Comicvine API endpoint.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.
            skip_cache: Skip read and writing to the cache.

        Returns:
            Json response from the Comicvine API.

        Raises:
            ServiceError: If there is an issue with the request or response from the Comicvine API.
            AuthenticationError: If Comicvine returns with an invalid API key response.
            CacheError: If it is unable to retrieve or push to the Cache correctly.
        """
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        params["format"] = "json"

        url = self.API_URL + endpoint
        cache_params = f"?{urlencode({k: params[k] for k in sorted(params)})}"
        cache_key = f"{url}{cache_params}"
        cache_key = re.sub(r"(.+api_key=)(.+?)(&.+)", r"\1*****\3", cache_key)

        if self.cache and not skip_cache:
            try:
                if cached_response := self.cache.select(query=cache_key):
                    return cached_response
            except AttributeError as err:
                raise CacheError(
                    f"Cache object passed in is missing attribute: {repr(err)}",
                ) from err

        response = self._perform_get_request(url=url, params=params)
        if "error" in response and response["error"] != "OK":
            raise ServiceError(response["error"])

        if self.cache and not skip_cache:
            try:
                self.cache.insert(query=cache_key, response=response)
            except AttributeError as err:
                raise CacheError(
                    f"Cache object passed in is missing attribute: {repr(err)}",
                ) from err

        return response

    def get_publisher(self, publisher_id: int) -> Publisher:
        """
        Request data for a Publisher based on its id.

        Args:
            publisher_id: The Publisher id.

        Returns:
            A Publisher object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/publisher/{ComicvineResource.PUBLISHER.resource_id}-{publisher_id}",
            )["results"]
            return parse_obj_as(Publisher, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def publisher(self, publisher_id: int) -> Publisher:
        """
        Request data for a Publisher based on its id.

        **DEPRECATED**: Use get_publisher()

        Args:
            publisher_id: The Publisher id.

        Returns:
            A Publisher object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.get_publisher(publisher_id=publisher_id)

    def list_publishers(
        self,
        params: Optional[Dict[str, Any]] = None,
        max_results: int = 500,
    ) -> List[PublisherEntry]:
        """
        Request data for a list of Publishers.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of PublisherEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/publishers/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[PublisherEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def publisher_list(
        self,
        params: Optional[Dict[str, Any]] = None,
        max_results: int = 500,
    ) -> List[PublisherEntry]:
        """
        Request data for a list of Publishers.

        **DEPRECATED**: Use list_publishers()

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of PublisherEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.list_publishers(params=params, max_results=max_results)

    def get_volume(self, volume_id: int) -> Volume:
        """
        Request data for a Volume based on its id.

        Args:
            volume_id: The Volume id.

        Returns:
            A Volume object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/volume/{ComicvineResource.VOLUME.resource_id}-{volume_id}",
            )["results"]
            return parse_obj_as(Volume, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def volume(self, volume_id: int) -> Volume:
        """
        Request data for a Volume based on its id.

        **DEPRECATED**: Use get_volume()

        Args:
            volume_id: The Volume id.

        Returns:
            A Volume object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.get_volume(volume_id=volume_id)

    def list_volumes(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[VolumeEntry]:
        """
        Request data for a list of Volumes.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of VolumeEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/volumes/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[VolumeEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def volume_list(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[VolumeEntry]:
        """
        Request data for a list of Volumes.

        **DEPRECATED**: Use list_volumes()

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of VolumeEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.list_volumes(params=params, max_results=max_results)

    def get_issue(self, issue_id: int) -> Issue:
        """
        Request data for an Issue based on its id.

        Args:
            issue_id: The Issue id.

        Returns:
            A Issue object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/issue/{ComicvineResource.ISSUE.resource_id}-{issue_id}",
            )["results"]
            return parse_obj_as(Issue, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def issue(self, issue_id: int) -> Issue:
        """
        Request data for an Issue based on its id.

        **DEPRECATED**: Use get_issue()

        Args:
            issue_id: The Issue id.

        Returns:
            A Issue object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.get_issue(issue_id=issue_id)

    def list_issues(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[IssueEntry]:
        """
        Request data for a list of Issues.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of IssueEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/issues/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[IssueEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def issue_list(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[IssueEntry]:
        """
        Request data for a list of Issues.

        **DEPRECATED**: Use list_issues()

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of IssueEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.list_issues(params=params, max_results=max_results)

    def get_story_arc(self, story_arc_id: int) -> StoryArc:
        """
        Request data for a Story Arc based on its id.

        Args:
            story_arc_id: The StoryArc id.

        Returns:
            A StoryArc object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/story_arc/{ComicvineResource.STORY_ARC.resource_id}-{story_arc_id}",
            )["results"]
            return parse_obj_as(StoryArc, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def story_arc(self, story_arc_id: int) -> StoryArc:
        """
        Request data for a Story Arc based on its id.

        **DEPRECATED**: Use get_story_arc()

        Args:
            story_arc_id: The StoryArc id.

        Returns:
            A StoryArc object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.get_story_arc(story_arc_id=story_arc_id)

    def list_story_arcs(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[StoryArcEntry]:
        """
        Request data for a list of Story Arcs.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of StoryArcEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/story_arcs/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[StoryArcEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def story_arc_list(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[StoryArcEntry]:
        """
        Request data for a list of Story Arcs.

        **DEPRECATED**: Use list_story_arcs()

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of StoryArcEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.list_story_arcs(params=params, max_results=max_results)

    def get_creator(self, creator_id: int) -> Creator:
        """
        Request data for a Creator based on its id.

        Args:
            creator_id: The Creator id.

        Returns:
            A Creator object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/person/{ComicvineResource.CREATOR.resource_id}-{creator_id}",
            )["results"]
            return parse_obj_as(Creator, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def creator(self, creator_id: int) -> Creator:
        """
        Request data for a Creator based on its id.

        **DEPRECATED**: Use get_creator()

        Args:
            creator_id: The Creator id.

        Returns:
            A Creator object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.get_creator(creator_id=creator_id)

    def list_creators(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[CreatorEntry]:
        """
        Request data for a list of Creators.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of CreatorEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/people/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[CreatorEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def creator_list(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[CreatorEntry]:
        """
        Request data for a list of Creators.

        **DEPRECATED**: Use list_creators()

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of CreatorEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.list_creators(params=params, max_results=max_results)

    def get_character(self, character_id: int) -> Character:
        """
        Request data for a Character based on its id.

        Args:
            character_id: The Character id.

        Returns:
            A Character object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/character/{ComicvineResource.CHARACTER.resource_id}-{character_id}",
            )["results"]
            return parse_obj_as(Character, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def character(self, character_id: int) -> Character:
        """
        Request data for a Character based on its id.

        **DEPRECATED**: Use get_character()

        Args:
            character_id: The Character id.

        Returns:
            A Character object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.get_character(character_id=character_id)

    def list_characters(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[CharacterEntry]:
        """
        Request data for a list of Characters.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of CharacterEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/characters/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[CharacterEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def character_list(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[CharacterEntry]:
        """
        Request data for a list of Characters.

        **DEPRECATED**: Use list_characters()

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of CharacterEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.list_characters(params=params, max_results=max_results)

    def get_team(self, team_id: int) -> Team:
        """
        Request data for a Team based on its id.

        Args:
            team_id: The Team id.

        Returns:
            A Team object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/team/{ComicvineResource.TEAM.resource_id}-{team_id}",
            )["results"]
            return parse_obj_as(Team, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def team(self, team_id: int) -> Team:
        """
        Request data for a Team based on its id.

        **DEPRECATED**: Use get_team()

        Args:
            team_id: The Team id.

        Returns:
            A Team object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.get_team(team_id=team_id)

    def list_teams(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[TeamEntry]:
        """
        Request data for a list of Teams.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of TeamEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/teams/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[TeamEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def team_list(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[TeamEntry]:
        """
        Request data for a list of Teams.

        **DEPRECATED**: Use list_teams()

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of TeamEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.list_teams(params=params, max_results=max_results)

    def get_location(self, location_id: int) -> Location:
        """
        Request data for a Location based on its id.

        Args:
            location_id: The Location id.

        Returns:
            A Location object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/location/{ComicvineResource.LOCATION.resource_id}-{location_id}",
            )["results"]
            return parse_obj_as(Location, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def location(self, location_id: int) -> Location:
        """
        Request data for a Location based on its id.

        **DEPRECATED**: Use get_location()

        Args:
            location_id: The Location id.

        Returns:
            A Location object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.get_location(location_id=location_id)

    def list_locations(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[LocationEntry]:
        """
        Request data for a list of Locations.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of LocationEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/locations/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[LocationEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def location_list(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[LocationEntry]:
        """
        Request data for a list of Locations.

        **DEPRECATED**: Use list_locations()

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of LocationEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.list_locations(params=params, max_results=max_results)

    def get_concept(self, concept_id: int) -> Concept:
        """
        Request data for a Concept based on its id.

        Args:
            concept_id: The Concept id.

        Returns:
            A Concept object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/concept/{ComicvineResource.CONCEPT.resource_id}-{concept_id}",
            )["results"]
            return parse_obj_as(Concept, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def concept(self, concept_id: int) -> Concept:
        """
        Request data for a Concept based on its id.

        **DEPRECATED**: Use get_concept()

        Args:
            concept_id: The Concept id.

        Returns:
            A Concept object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.get_concept(concept_id=concept_id)

    def list_concepts(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[ConceptEntry]:
        """
        Request data for a list of Concepts.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of ConceptEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/concepts/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[ConceptEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def concept_list(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[ConceptEntry]:
        """
        Request data for a list of Concepts.

        **DEPRECATED**: Use list_concepts()

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of ConceptEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        return self.list_concepts(params=params, max_results=max_results)

    def get_power(self, power_id: int) -> Power:
        """
        Request data for a Power based on its id.

        Args:
            power_id: The Power id.

        Returns:
            A Power object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/power/{ComicvineResource.POWER.resource_id}-{power_id}",
            )["results"]
            return parse_obj_as(Power, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_powers(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[PowerEntry]:
        """
        Request data for a list of Powers.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of PowerEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/powers/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[PowerEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_origin(self, origin_id: int) -> Origin:
        """
        Request data for an Origin based on its id.

        Args:
            origin_id: The Origin id.

        Returns:
            A Origin object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/origin/{ComicvineResource.ORIGIN.resource_id}-{origin_id}",
            )["results"]
            return parse_obj_as(Origin, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_origins(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[OriginEntry]:
        """
        Request data for a list of Origins.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of OriginEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/origins/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[OriginEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_item(self, item_id: int) -> Item:
        """
        Request data for an Item based on its id.

        Args:
            item_id: The Item id.

        Returns:
            A Item object
        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._get_request(
                endpoint=f"/object/{ComicvineResource.ITEM.resource_id}-{item_id}",
            )["results"]
            return parse_obj_as(Item, result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_items(
        self,
        params: Optional[Dict[str, Union[str, int]]] = None,
        max_results: int = 500,
    ) -> List[ItemEntry]:
        """
        Request data for a list of Items.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of ItemEntry objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_offset_results(
                endpoint="/objects/",
                params=params,
                max_results=max_results,
            )
            return parse_obj_as(List[ItemEntry], results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def search(
        self,
        resource: ComicvineResource,
        query: str,
        max_results: int = 500,
    ) -> Union[
        List[PublisherEntry],
        List[VolumeEntry],
        List[IssueEntry],
        List[StoryArcEntry],
        List[CreatorEntry],
        List[CharacterEntry],
        List[TeamEntry],
        List[LocationEntry],
        List[ConceptEntry],
        List[PowerEntry],
        List[OriginEntry],
        List[ItemEntry],
    ]:
        """
        Request a list of search results filtered by provided resource.

        Args:
            resource: Filter which type of resource to return.
            query: Search query string.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of results, mapped to the given resource.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._retrieve_page_results(
                endpoint="/search/",
                params={"query": query, "resources": resource.search_resource},
                max_results=max_results,
            )
            return parse_obj_as(resource.search_response, results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def _retrieve_page_results(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        max_results: int = 500,
    ) -> List[Dict[str, Any]]:
        """
        Get responses until all the results are collected.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Json response results.
        """
        if params is None:
            params = {}
        params["page"] = 1
        params["limit"] = 100
        response = self._get_request(endpoint=endpoint, params=params)
        results = response["results"]
        while (
            response["results"]
            and len(results) < response["number_of_total_results"]
            and len(results) < max_results
        ):
            params["page"] += 1
            response = self._get_request(endpoint=endpoint, params=params)
            results.extend(response["results"])
        return results[:max_results]

    def _retrieve_offset_results(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        max_results: int = 500,
    ) -> List[Dict[str, Any]]:
        """
        Get responses until all the results are collected.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Json response results.
        """
        if params is None:
            params = {}
        params["limit"] = 100
        response = self._get_request(endpoint=endpoint, params=params)
        results = response["results"]
        while (
            response["results"]
            and len(results) < response["number_of_total_results"]
            and len(results) < max_results
        ):
            params["offset"] = len(results)
            response = self._get_request(endpoint=endpoint, params=params)
            results.extend(response["results"])
        return results[:max_results]
