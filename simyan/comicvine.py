"""The Comicvine module.

This module provides the following classes:
- Comicvine
- ComicvineResource
"""

__all__ = ["Comicvine", "ComicvineResource"]

import logging
import platform
from enum import Enum
from json import JSONDecodeError
from typing import Any, Final, TypeVar
from urllib.parse import urlencode, urlparse

from httpx import (
    Client,
    HTTPStatusError,
    HTTPTransport,
    Request,
    RequestError,
    Response,
    TimeoutException,
)
from pydantic import TypeAdapter, ValidationError
from pyrate_limiter import AbstractBucket, Duration, Limiter, Rate, SQLiteBucket

from simyan import __version__
from simyan.exceptions import AuthenticationError, RateLimitError, ServiceError
from simyan.schemas.character import BasicCharacter, Character
from simyan.schemas.concept import BasicConcept, Concept
from simyan.schemas.creator import BasicCreator, Creator
from simyan.schemas.issue import BasicIssue, Issue
from simyan.schemas.item import BasicItem, Item
from simyan.schemas.location import BasicLocation, Location
from simyan.schemas.origin import BasicOrigin, Origin
from simyan.schemas.power import BasicPower, Power
from simyan.schemas.publisher import BasicPublisher, Publisher
from simyan.schemas.story_arc import BasicStoryArc, StoryArc
from simyan.schemas.team import BasicTeam, Team
from simyan.schemas.volume import BasicVolume, Volume
from simyan.sqlite_cache import SQLiteCache

# Constants
LOGGER = logging.getLogger(__name__)
T = TypeVar("T")
RATELIMIT_BUCKET: Final[AbstractBucket] = SQLiteBucket.init_from_file(
    [Rate(1, Duration.SECOND), Rate(200, Duration.HOUR)]
)


class RateLimiterTransport(HTTPTransport):
    def __init__(self, limiter: Limiter, **kwargs):  # noqa: ANN003
        super().__init__(**kwargs)
        self.limiter = limiter

    def handle_request(self, request: Request, **kwargs) -> Response:  # noqa: ANN003
        parts = request.url.path.strip("/").split("/")
        if len(parts) == 3:
            name = f"get_{parts[1]}"
        elif len(parts) == 2:
            name = parts[1]
        else:
            name = "comicvine"
        self.limiter.try_acquire(name)
        LOGGER.debug("Acquired lock")
        return super().handle_request(request, **kwargs)


def rate_mapping(*args: Any, **kwargs: Any) -> tuple[str, int]:
    if kwargs and "url" in kwargs:
        url = kwargs["url"]
    else:
        return "comicvine", 1
    parts = urlparse(url).path.strip("/").split("/")
    if not parts or len(parts) < 2:
        return "comicvine", 1
    if len(parts) == 3:
        return f"get_{parts[1]}", 1
    return parts[1], 1


class ComicvineResource(Enum):
    """Enum class for Comicvine Resources."""

    ISSUE = (4000, "issue", list[BasicIssue])
    """"""
    CHARACTER = (4005, "character", list[BasicCharacter])
    """"""
    PUBLISHER = (4010, "publisher", list[BasicPublisher])
    """"""
    CONCEPT = (4015, "concept", list[BasicConcept])
    """"""
    LOCATION = (4020, "location", list[BasicLocation])
    """"""
    ORIGIN = (4030, "origin", list[BasicOrigin])
    """"""
    POWER = (4035, "power", list[BasicPower])
    """"""
    CREATOR = (4040, "person", list[BasicCreator])
    """"""
    STORY_ARC = (4045, "story_arc", list[BasicStoryArc])
    """"""
    VOLUME = (4050, "volume", list[BasicVolume])
    """"""
    ITEM = (4055, "object", list[BasicItem])
    """"""
    TEAM = (4060, "team", list[BasicTeam])
    """"""

    @property
    def resource_id(self) -> int:
        """Start of id used by Comicvine to create unique ids."""
        return self.value[0]

    @property
    def search_resource(self) -> str:
        """Resource string for filtering searches."""
        return self.value[1]

    @property
    def search_response(self) -> type[T]:
        """Response type for resource when using a search endpoint."""
        return self.value[2]


class Comicvine:
    """Class with functionality to request Comicvine API endpoints.

    Args:
        api_key: User's API key to access the Comicvine API.
        timeout: Set how long requests will wait for a response (in seconds).
        cache: SQLiteCache to use if set.
        user_agent: Custom User-Agent string. If None, uses default Simyan User-Agent.
    """

    def __init__(
        self,
        api_key: str,
        cache: SQLiteCache | None,
        base_url: str = "https://comicvine.gamespot.com/api",
        user_agent: str | None = None,
        timeout: float = 30,
        limiter: Limiter = Limiter(RATELIMIT_BUCKET),  # noqa: B008
    ):
        self._base_url = base_url
        self._client = Client(
            base_url=self._base_url,
            headers={
                "Accept": "application/json",
                "User-Agent": user_agent
                or f"Simyan/{__version__} ({platform.system()}: {platform.release()}; Python v{platform.python_version()})",  # noqa: E501
            },
            params={"api_key": api_key, "format": "json"},
            timeout=timeout,
            transport=RateLimiterTransport(limiter),
        )
        self._cache = cache

    def _perform_get_request(
        self, endpoint: str, params: dict[str, str] | None = None
    ) -> dict[str, Any]:
        params: dict[str, str] = params or {}

        try:
            response = self._client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except RequestError as err:
            raise ServiceError(f"Unable to connect to '{self._base_url}{endpoint}'") from err
        except HTTPStatusError as err:
            try:
                if err.response.status_code == 401:
                    raise AuthenticationError(err.response.json()["error"]) from err
                if err.response.status_code == 404:
                    raise ServiceError("Resource not found") from err
                if err.response.status_code in (420, 429):
                    raise RateLimitError(err.response.json()["error"]) from err
                if err.response.status_code in (500, 502, 503):
                    raise ServiceError("Service error, retry again later") from err
                raise ServiceError(err.response.json()["error"]) from err
            except JSONDecodeError as err:
                raise ServiceError(
                    f"Unable to parse response from '{self._base_url}{endpoint}' as Json"
                ) from err
        except JSONDecodeError as err:
            raise ServiceError(
                f"Unable to parse response from '{self._base_url}{endpoint}' as Json"
            ) from err
        except TimeoutException as err:
            raise ServiceError("Service took too long to respond") from err

    def _get_request(self, endpoint: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        params: dict[str, str] = params or {}
        url = f"{self._base_url}{endpoint}/"
        cache_params = f"?{urlencode({k: params[k] for k in sorted(params)})}"
        cache_key = url + cache_params

        if self._cache:
            cache_data = self._cache.select(query=cache_key)
            if cache_data:
                return cache_data
        response = self._perform_get_request(endpoint=endpoint + "/", params=params)
        if "error" in response and response["error"] != "OK":
            raise ServiceError(response["error"])
        if self._cache:
            self._cache.insert(query=cache_key, response=response)
        return response

    def _fetch_item(self, endpoint: str) -> dict[str, Any]:
        return self._get_request(endpoint=endpoint)["results"]

    def _fetch_paged_list(
        self, endpoint: str, max_results: int, params: dict[str, str] | None = None
    ) -> list[dict[str, Any]]:
        params: dict[str, str] = params or {}
        params["limit"] = params.get("limit", "100")
        results: list[dict[str, Any]] = []
        page = int(params.get("page", "1"))
        while True:
            response = self._get_request(endpoint=endpoint, params={**params, "page": str(page)})
            results.extend(response["results"])
            page += 1
            if not response["results"] or len(results) >= max_results:
                break
        return results[:max_results]

    def _fetch_offset_list(
        self, endpoint: str, max_results: int, params: dict[str, str] | None = None
    ) -> list[dict[str, Any]]:
        params: dict[str, str] = params or {}
        params["limit"] = params.get("limit", "100")
        results: list[dict[str, Any]] = []
        offset = int(params.get("offset", "0"))
        while True:
            response = self._get_request(
                endpoint=endpoint, params={**params, "offset": str(offset)}
            )
            results.extend(response["results"])
            offset += int(params["limit"])
            if not response["results"] or len(results) >= max_results:
                break
        return results[:max_results]

    def list_publishers(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicPublisher]:
        """Request a list of Publishers.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Publisher objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/publishers", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicPublisher]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_publisher(self, publisher_id: int) -> Publisher:
        """Request a Publisher using its id.

        Args:
            publisher_id: The Publisher id.

        Returns:
            A Publisher object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/publisher/{ComicvineResource.PUBLISHER.resource_id}-{publisher_id}"
            )
            return TypeAdapter(Publisher).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_volumes(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicVolume]:
        """Request a list of Volumes.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Volume objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/volumes", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicVolume]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_volume(self, volume_id: int) -> Volume:
        """Request a Volume using its id.

        Args:
            volume_id: The Volume id.

        Returns:
            A Volume object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/volume/{ComicvineResource.VOLUME.resource_id}-{volume_id}"
            )
            return TypeAdapter(Volume).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_issues(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicIssue]:
        """Request a list of Issues.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Issue objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/issues", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicIssue]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_issue(self, issue_id: int) -> Issue:
        """Request an Issue using its id.

        Args:
            issue_id: The Issue id.

        Returns:
            A Issue object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/issue/{ComicvineResource.ISSUE.resource_id}-{issue_id}"
            )
            return TypeAdapter(Issue).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_story_arcs(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicStoryArc]:
        """Request a list of Story Arcs.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of StoryArc objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/story_arcs", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicStoryArc]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_story_arc(self, story_arc_id: int) -> StoryArc:
        """Request a Story Arc using its id.

        Args:
            story_arc_id: The StoryArc id.

        Returns:
            A StoryArc object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/story_arc/{ComicvineResource.STORY_ARC.resource_id}-{story_arc_id}"
            )
            return TypeAdapter(StoryArc).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_creators(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicCreator]:
        """Request a list of Creators.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Creator objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/people", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicCreator]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_creator(self, creator_id: int) -> Creator:
        """Request a Creator using its id.

        Args:
            creator_id: The Creator id.

        Returns:
            A Creator object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/person/{ComicvineResource.CREATOR.resource_id}-{creator_id}"
            )
            return TypeAdapter(Creator).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_characters(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicCharacter]:
        """Request a list of Characters.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Character objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/characters", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicCharacter]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_character(self, character_id: int) -> Character:
        """Request a Character using its id.

        Args:
            character_id: The Character id.

        Returns:
            A Character object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/character/{ComicvineResource.CHARACTER.resource_id}-{character_id}"
            )
            return TypeAdapter(Character).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_teams(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicTeam]:
        """Request a list of Teams.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Team objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/teams", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicTeam]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_team(self, team_id: int) -> Team:
        """Request a Team using its id.

        Args:
            team_id: The Team id.

        Returns:
            A Team object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/team/{ComicvineResource.TEAM.resource_id}-{team_id}"
            )
            return TypeAdapter(Team).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_locations(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicLocation]:
        """Request a list of Locations.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Location objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/locations", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicLocation]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_location(self, location_id: int) -> Location:
        """Request a Location using its id.

        Args:
            location_id: The Location id.

        Returns:
            A Location object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/location/{ComicvineResource.LOCATION.resource_id}-{location_id}"
            )
            return TypeAdapter(Location).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_concepts(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicConcept]:
        """Request a list of Concepts.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Concept objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/concepts", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicConcept]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_concept(self, concept_id: int) -> Concept:
        """Request a Concept using its id.

        Args:
            concept_id: The Concept id.

        Returns:
            A Concept object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/concept/{ComicvineResource.CONCEPT.resource_id}-{concept_id}"
            )
            return TypeAdapter(Concept).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_powers(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicPower]:
        """Request a list of Powers.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Power objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/powers", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicPower]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_power(self, power_id: int) -> Power:
        """Request a Power using its id.

        Args:
            power_id: The Power id.

        Returns:
            A Power object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/power/{ComicvineResource.POWER.resource_id}-{power_id}"
            )
            return TypeAdapter(Power).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_origins(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicOrigin]:
        """Request a list of Origins.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Origin objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/origins", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicOrigin]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_origin(self, origin_id: int) -> Origin:
        """Request an Origin using its id.

        Args:
            origin_id: The Origin id.

        Returns:
            An Origin object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/origin/{ComicvineResource.ORIGIN.resource_id}-{origin_id}"
            )
            return TypeAdapter(Origin).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def list_items(
        self, params: dict[str, Any] | None = None, max_results: int = 500
    ) -> list[BasicItem]:
        """Request a list of Items.

        Args:
            params: Parameters to add to the request.
            max_results: Limits the amount of results looked up and returned.

        Returns:
            A list of Item objects.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            results = self._fetch_offset_list(
                endpoint="/objects", params=params, max_results=max_results
            )
            return TypeAdapter(list[BasicItem]).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err

    def get_item(self, item_id: int) -> Item:
        """Request an Item using its id.

        Args:
            item_id: The Item id.

        Returns:
            An Item object or None if not found.

        Raises:
            ServiceError: If there is an issue with validating the response.
        """
        try:
            result = self._fetch_item(
                endpoint=f"/object/{ComicvineResource.ITEM.resource_id}-{item_id}"
            )
            return TypeAdapter(Item).validate_python(result)
        except ValidationError as err:
            raise ServiceError(err) from err

    def search(
        self, resource: ComicvineResource, query: str, max_results: int = 500
    ) -> (
        list[BasicPublisher]
        | list[BasicVolume]
        | list[BasicIssue]
        | list[BasicStoryArc]
        | list[BasicCreator]
        | list[BasicCharacter]
        | list[BasicTeam]
        | list[BasicLocation]
        | list[BasicConcept]
        | list[BasicPower]
        | list[BasicOrigin]
        | list[BasicItem]
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
            results = self._fetch_paged_list(
                endpoint="/search",
                params={"query": query, "resources": resource.search_resource},
                max_results=max_results,
            )
            return TypeAdapter(resource.search_response).validate_python(results)
        except ValidationError as err:
            raise ServiceError(err) from err
