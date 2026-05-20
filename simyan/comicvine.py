__all__ = ["Comicvine", "ComicvineResource"]

import platform
from datetime import timedelta
from enum import Enum
from http import HTTPStatus
from pathlib import Path
from typing import Any, TypeVar
from urllib.parse import urlparse

from pydantic import TypeAdapter, ValidationError
from requests.exceptions import HTTPError, JSONDecodeError, RequestException, Timeout
from requests.models import PreparedRequest
from requests.sessions import Session
from requests_cache import NEVER_EXPIRE, CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, SQLiteBucket

from simyan import __version__, get_cache_root
from simyan.errors import AuthenticationError, RateLimitError, ServiceError
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

T = TypeVar("T")


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    def _bucket_name(self, request: PreparedRequest) -> str:
        parts = urlparse(request.url).path.strip("/").split("/") if request.url else []
        if len(parts) == 3:
            return f"get_{parts[1]}"
        if len(parts) == 2:
            return parts[1]
        return self.bucket_name or "comicvine"


class ComicvineResource(Enum):
    """Enum class for Comicvine Resources.

    Attributes:
        ISSUE:
        CHARACTER:
        PUBLISHER:
        CONCEPT:
        LOCATION:
        ORIGIN:
        POWER:
        CREATOR:
        STORY_ARC:
        VOLUME:
        ITEM:
        TEAM:
    """

    ISSUE = (4000, "issue", list[BasicIssue])
    CHARACTER = (4005, "character", list[BasicCharacter])
    PUBLISHER = (4010, "publisher", list[BasicPublisher])
    CONCEPT = (4015, "concept", list[BasicConcept])
    LOCATION = (4020, "location", list[BasicLocation])
    ORIGIN = (4030, "origin", list[BasicOrigin])
    POWER = (4035, "power", list[BasicPower])
    CREATOR = (4040, "person", list[BasicCreator])
    STORY_ARC = (4045, "story_arc", list[BasicStoryArc])
    VOLUME = (4050, "volume", list[BasicVolume])
    ITEM = (4055, "object", list[BasicItem])
    TEAM = (4060, "team", list[BasicTeam])

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
        """Response type for a resource when using a search endpoint."""
        return self.value[2]


class Comicvine:
    """Class with functionality to request Comicvine API endpoints.

    Args:
        api_key: User's API key to access the Comicvine API.
        base_url: Root URL of the Comicvine API.
        user_agent: Value sent in the `User-Agent` request header.
        timeout: Set how long requests will wait for a response (in seconds).
        cache_path: Path to the SQLite cache file.
            If not provided, a default path will be used under ~/.cache/simyan/cache.sqlite
        cache_expiry: Duration for which cached responses are valid.
            Response cache-headers take precedence.
        ratelimit_path: Path to the SQLite ratelimit file.
            If not provided, a default path will be used under ~/.cache/simyan/ratelimits.sqlite
    """

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        user_agent: str | None = None,
        timeout: float = 20,
        cache_path: Path | None = None,
        cache_expiry: timedelta = timedelta(days=14),
        ratelimit_path: Path | None = None,
    ):
        self._base_url = base_url or "https://comicvine.gamespot.com/api"
        self._session = CachedLimiterSession(
            backend=SQLiteCache(
                db_path=cache_path or (get_cache_root() / "cache.sqlite"), serializer="json"
            ),
            expire_after=cache_expiry,
            cache_control=cache_expiry != NEVER_EXPIRE,
            ignored_parameters=["api_key"],
            per_second=1,
            per_hour=200,
            max_delay=timeout * 2,
            bucket_class=SQLiteBucket,
            bucket_kwargs={"path": ratelimit_path or (get_cache_root() / "ratelimits.sqlite")},
            per_host=False,
            bucket_name="comicvine",
        )
        self._session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": user_agent
                or f"Simyan/{__version__} ({platform.system()}: {platform.release()}; Python v{platform.python_version()})",  # noqa: E501
            }
        )
        self._session.params.update({"api_key": api_key, "format": "json"})
        self._timeout = timeout

    def _get_request(self, endpoint: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        params: dict[str, str] = params or {}

        try:
            response = self._session.get(
                url=f"{self._base_url}{endpoint}/", params=params, timeout=self._timeout
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as err:
            status_code = (
                HTTPStatus.INTERNAL_SERVER_ERROR
                if err.response is None
                else err.response.status_code
            )
            try:
                response = {} if err.response is None else err.response.json()
                if status_code == HTTPStatus.UNAUTHORIZED:
                    raise AuthenticationError(response.get("error")) from err
                if status_code == HTTPStatus.NOT_FOUND:
                    raise ServiceError("Resource not found") from err
                if status_code in (HTTPStatus.TOO_MANY_REQUESTS, 420):
                    raise RateLimitError(response.get("error")) from err
                raise ServiceError(f"{status_code}: {response}") from err
            except JSONDecodeError as err:
                raise ServiceError(
                    f"{status_code}: Unable to parse response from '{self._base_url}{endpoint}/' as Json"  # noqa: E501
                ) from err
        except Timeout as err:
            raise ServiceError("Service took too long to respond") from err
        except RequestException as err:
            raise ServiceError(f"Unable to connect to '{self._base_url}{endpoint}/'") from err
        except JSONDecodeError as err:
            raise ServiceError(
                f"Unable to parse response from '{self._base_url}{endpoint}/' as Json"
            ) from err

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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Publisher objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Volume objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Issue objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of StoryArc objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Creator objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Character objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Team objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Location objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Concept objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Power objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Origin objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of Item objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
        """Request a list of search results filtered by the provided resource.

        Args:
            resource: Filter which type of resource to return.
            query: Search query string.
            max_results: Limits the number of results looked up and returned.

        Returns:
            A list of results, mapped to the given resource.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
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
