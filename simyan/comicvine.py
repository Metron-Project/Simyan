"""The Comicvine module.

This module provides the following classes:

- ComicvineResource
- Comicvine
"""
from __future__ import annotations

__all__ = ["ComicvineResource", "Comicvine"]
import platform
import re
from enum import Enum
from json import JSONDecodeError
from typing import TYPE_CHECKING, Any, List, TypeVar
from urllib.parse import urlencode

from pydantic import TypeAdapter, ValidationError
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

if TYPE_CHECKING:
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
    def resource_id(self: ComicvineResource) -> int:
        """Start of id used by Comicvine to create unique ids."""
        return self.value[0]

    @property
    def search_resource(self: ComicvineResource) -> str:
        """Resource string for filtering searches."""
        return self.value[1]

    @property
    def search_response(self: ComicvineResource) -> type[T]:
        """Response type for resource when using a search endpoint."""
        return self.value[2]


class Comicvine:
    """Comicvine to request Comicvine API endpoints.

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

    def __init__(
        self: Comicvine,
        api_key: str,
        timeout: int = 30,
        cache: SQLiteCache | None = None,
    ):
        self.headers = {
            "Accept": "application/json",
            "User-Agent": f"Simyan/{__version__}/{platform.system()}: {platform.release()}",
        }
        self.api_key = api_key
        self.timeout = timeout
        self.cache = cache

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _perform_get_request(
        self: Comicvine,
        url: str,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make GET request to Comicvine API endpoint.

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
            msg = f"Unable to connect to `{url}`"
            raise ServiceError(msg) from err
        except HTTPError as err:
            if err.response.status_code == 401:
                msg = "Invalid API Key"
                raise AuthenticationError(msg) from err
            if err.response.status_code == 404:
                msg = "Unknown endpoint"
                raise ServiceError(msg) from err
            if err.response.status_code == 502:
                msg = "Service error, retry again in 30s"
                raise ServiceError(msg) from err
            raise ServiceError(err.response.json()["error"]) from err
        except JSONDecodeError as err:
            msg = f"Unable to parse response from `{url}` as Json"
            raise ServiceError(msg) from err
        except ReadTimeout as err:
            msg = "Service took too long to respond"
            raise ServiceError(msg) from err

    def _get_request(
        self: Comicvine,
        endpoint: str,
        params: dict[str, str] | None = None,
        skip_cache: bool = False,
    ) -> dict[str, Any]:
        """Check cache or make GET request to Comicvine API endpoint.

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
                msg = f"Cache object passed in is missing attribute: {err!r}"
                raise CacheError(msg) from err

        response = self._perform_get_request(url=url, params=params)
        if "error" in response and response["error"] != "OK":
            raise ServiceError(response["error"])

        if self.cache and not skip_cache:
            try:
                self.cache.insert(query=cache_key, response=response)
            except AttributeError as err:
                msg = f"Cache object passed in is missing attribute: {err!r}"
                raise CacheError(msg) from err

        return response

    def get_publisher(self: Comicvine, publisher_id: int) -> Publisher:
        """Request data for a Publisher based on its id.

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
            adapter = TypeAdapter(Publisher)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_publishers(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[PublisherEntry]:
        """Request data for a list of Publishers.

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
            adapter = TypeAdapter(List[PublisherEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_volume(self: Comicvine, volume_id: int) -> Volume:
        """Request data for a Volume based on its id.

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
            adapter = TypeAdapter(Volume)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_volumes(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[VolumeEntry]:
        """Request data for a list of Volumes.

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
            adapter = TypeAdapter(List[VolumeEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_issue(self: Comicvine, issue_id: int) -> Issue:
        """Request data for an Issue based on its id.

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
            adapter = TypeAdapter(Issue)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_issues(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[IssueEntry]:
        """Request data for a list of Issues.

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
            adapter = TypeAdapter(List[IssueEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_story_arc(self: Comicvine, story_arc_id: int) -> StoryArc:
        """Request data for a Story Arc based on its id.

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
            adapter = TypeAdapter(StoryArc)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_story_arcs(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[StoryArcEntry]:
        """Request data for a list of Story Arcs.

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
            adapter = TypeAdapter(List[StoryArcEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_creator(self: Comicvine, creator_id: int) -> Creator:
        """Request data for a Creator based on its id.

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
            adapter = TypeAdapter(Creator)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_creators(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[CreatorEntry]:
        """Request data for a list of Creators.

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
            adapter = TypeAdapter(List[CreatorEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_character(self: Comicvine, character_id: int) -> Character:
        """Request data for a Character based on its id.

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
            adapter = TypeAdapter(Character)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_characters(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[CharacterEntry]:
        """Request data for a list of Characters.

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
            adapter = TypeAdapter(List[CharacterEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_team(self: Comicvine, team_id: int) -> Team:
        """Request data for a Team based on its id.

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
            adapter = TypeAdapter(Team)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_teams(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[TeamEntry]:
        """Request data for a list of Teams.

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
            adapter = TypeAdapter(List[TeamEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_location(self: Comicvine, location_id: int) -> Location:
        """Request data for a Location based on its id.

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
            adapter = TypeAdapter(Location)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_locations(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[LocationEntry]:
        """Request data for a list of Locations.

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
            adapter = TypeAdapter(List[LocationEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_concept(self: Comicvine, concept_id: int) -> Concept:
        """Request data for a Concept based on its id.

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
            adapter = TypeAdapter(Concept)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_concepts(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[ConceptEntry]:
        """Request data for a list of Concepts.

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
            adapter = TypeAdapter(List[ConceptEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_power(self: Comicvine, power_id: int) -> Power:
        """Request data for a Power based on its id.

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
            adapter = TypeAdapter(Power)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_powers(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[PowerEntry]:
        """Request data for a list of Powers.

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
            adapter = TypeAdapter(List[PowerEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_origin(self: Comicvine, origin_id: int) -> Origin:
        """Request data for an Origin based on its id.

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
            adapter = TypeAdapter(Origin)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_origins(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[OriginEntry]:
        """Request data for a list of Origins.

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
            adapter = TypeAdapter(List[OriginEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_item(self: Comicvine, item_id: int) -> Item:
        """Request data for an Item based on its id.

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
            adapter = TypeAdapter(Item)
            return adapter.validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_items(
        self: Comicvine,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[ItemEntry]:
        """Request data for a list of Items.

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
            adapter = TypeAdapter(List[ItemEntry])
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def search(
        self: Comicvine,
        resource: ComicvineResource,
        query: str,
        max_results: int = 500,
    ) -> (
        list[PublisherEntry]
        | list[VolumeEntry]
        | list[IssueEntry]
        | list[StoryArcEntry]
        | list[CreatorEntry]
        | list[CharacterEntry]
        | list[TeamEntry]
        | list[LocationEntry]
        | list[ConceptEntry]
        | list[PowerEntry]
        | list[OriginEntry]
        | list[ItemEntry]
    ):
        """Request a list of search results filtered by provided resource.

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
            adapter = TypeAdapter(resource.search_response)
            return adapter.validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def _retrieve_page_results(
        self: Comicvine,
        endpoint: str,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[dict[str, Any]]:
        """Get responses until all the results are collected.

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
        self: Comicvine,
        endpoint: str,
        params: dict[str, Any] | None = None,
        max_results: int = 500,
    ) -> list[dict[str, Any]]:
        """Get responses until all the results are collected.

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
