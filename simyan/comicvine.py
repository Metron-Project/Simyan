__all__ = ["Comicvine", "ComicvineResource"]

import platform
from datetime import timedelta
from enum import Enum
from http import HTTPStatus
from pathlib import Path
from typing import Any, Literal, TypeVar
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

try:
    from typing import deprecated  # Python >= 3.13  # ty:ignore[unresolved-import]
except ImportError:
    from typing_extensions import deprecated

T = TypeVar("T")
HttpMethod = Literal["GET"]


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

    ISSUE = (4000, "issues", "issue", BasicIssue, Issue)
    CHARACTER = (4005, "characters", "character", BasicCharacter, Character)
    PUBLISHER = (4010, "publishers", "publisher", BasicPublisher, Publisher)
    CONCEPT = (4015, "concepts", "concept", BasicConcept, Concept)
    LOCATION = (4020, "locations", "location", BasicLocation, Location)
    ORIGIN = (4030, "origins", "origin", BasicOrigin, Origin)
    POWER = (4035, "powers", "power", BasicPower, Power)
    CREATOR = (4040, "people", "person", BasicCreator, Creator)
    STORY_ARC = (4045, "story_arcs", "story_arc", BasicStoryArc, StoryArc)
    VOLUME = (4050, "volumes", "volume", BasicVolume, Volume)
    ITEM = (4055, "objects", "object", BasicItem, Item)
    TEAM = (4060, "teams", "team", BasicTeam, Team)

    @property
    def resource_id(self) -> int:  # noqa: D102
        return self.value[0]

    @property
    def list_endpoint(self) -> str:  # noqa: D102
        return self.value[1]

    @property
    def item_endpoint(self) -> str:  # noqa: D102
        return self.value[2]

    @property
    def list_type(self) -> type[T]:  # noqa: D102
        return self.value[3]

    @property
    def item_type(self) -> type[T]:  # noqa: D102
        return self.value[4]


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

    def _request(
        self, method: HttpMethod, endpoint: str, params: dict[str, str] | None = None
    ) -> dict[str, Any]:
        url = f"{self._base_url}{endpoint}/"
        kwargs: dict[str, Any] = {"timeout": self._timeout}
        if params:
            kwargs["params"] = params
        try:
            response = self._session.request(method=method, url=url, **kwargs)
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
                    f"{status_code}: Unable to parse response from '{url}' as Json"
                ) from err
        except Timeout as err:
            raise ServiceError("Service took too long to respond") from err
        except RequestException as err:
            raise ServiceError(f"Unable to connect to '{url}'") from err
        except JSONDecodeError as err:
            raise ServiceError(f"Unable to parse response from '{url}' as Json") from err

    @staticmethod
    def _convert(data: dict[str, Any], type_: type[T]) -> T:
        try:
            return TypeAdapter(type_).validate_python(data)
        except ValidationError as err:
            raise ServiceError(err) from err

    def _offset(
        self, endpoint: str, params: dict[str, str] | None = None, max_results: int | None = None
    ) -> list[dict[str, Any]]:
        params = params or {}
        offset = int(params.get("offset", "0"))
        limit = int(params.get("limit", "100"))
        results = []
        while True:
            params["offset"] = str(offset)
            params["limit"] = str(limit)
            response = self._request(method="GET", endpoint=endpoint, params=params)
            if not response["results"]:
                return results
            results.extend(response["results"])
            if max_results is not None and len(results) >= max_results:
                return results[:max_results]
            offset += limit

    def _paginate(
        self, endpoint: str, params: dict[str, str] | None = None, max_results: int | None = None
    ) -> list[dict[str, Any]]:
        params = params or {}
        page = int(params.get("page", "1"))
        results = []
        while True:
            params["page"] = str(page)
            response = self._request(method="GET", endpoint=endpoint, params=params)
            if not response["results"]:
                return results
            results.extend(response["results"])
            if max_results is not None and len(results) >= max_results:
                return results[:max_results]
            page += 1

    def _get_item(self, resource: ComicvineResource, id_: int) -> T:
        return self._convert(
            data=self._request(
                method="GET", endpoint=f"/{resource.item_endpoint}/{resource.resource_id}-{id_}"
            )["results"],
            type_=resource.item_type,
        )

    def _get_list(
        self,
        resource: ComicvineResource,
        params: dict[str, str] | None = None,
        max_results: int | None = None,
    ) -> list[T]:
        data = self._offset(
            endpoint=f"/{resource.list_endpoint}", params=params, max_results=max_results
        )
        return [self._convert(data=x, type_=resource.list_type) for x in data]

    def _search(
        self, resource: ComicvineResource, query: str, max_results: int | None = None
    ) -> list[T]:
        params = {"query": query, "resources": resource.item_endpoint}
        data = self._paginate(endpoint="/search", params=params, max_results=max_results)
        return [self._convert(data=x, type_=resource.list_type) for x in data]

    def list_publishers(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicPublisher]:
        """Request a list of Publishers.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Publisher objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.PUBLISHER, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.PUBLISHER, id_=publisher_id)

    def search_publishers(self, query: str, max_results: int | None = 500) -> list[BasicPublisher]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of publisher results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(
            resource=ComicvineResource.PUBLISHER, query=query, max_results=max_results
        )

    def list_volumes(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicVolume]:
        """Request a list of Volumes.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Volume objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.VOLUME, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.VOLUME, id_=volume_id)

    def search_volumes(self, query: str, max_results: int | None = 500) -> list[BasicVolume]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of volume results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(resource=ComicvineResource.VOLUME, query=query, max_results=max_results)

    def list_issues(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicIssue]:
        """Request a list of Issues.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Issue objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.ISSUE, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.ISSUE, id_=issue_id)

    def search_issues(self, query: str, max_results: int | None = 500) -> list[BasicIssue]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of issue results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(resource=ComicvineResource.ISSUE, query=query, max_results=max_results)

    def list_story_arcs(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicStoryArc]:
        """Request a list of Story Arcs.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of StoryArc objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.STORY_ARC, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.STORY_ARC, id_=story_arc_id)

    def search_story_arcs(self, query: str, max_results: int | None = 500) -> list[BasicStoryArc]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of story arc results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(
            resource=ComicvineResource.STORY_ARC, query=query, max_results=max_results
        )

    def list_creators(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicCreator]:
        """Request a list of Creators.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Creator objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.CREATOR, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.CREATOR, id_=creator_id)

    def search_creators(self, query: str, max_results: int | None = 500) -> list[BasicCreator]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of creator results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(
            resource=ComicvineResource.CREATOR, query=query, max_results=max_results
        )

    def list_characters(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicCharacter]:
        """Request a list of Characters.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Character objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.CHARACTER, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.CHARACTER, id_=character_id)

    def search_characters(self, query: str, max_results: int | None = 500) -> list[BasicCharacter]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of character results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(
            resource=ComicvineResource.CHARACTER, query=query, max_results=max_results
        )

    def list_teams(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicTeam]:
        """Request a list of Teams.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Team objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.TEAM, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.TEAM, id_=team_id)

    def search_teams(self, query: str, max_results: int | None = 500) -> list[BasicTeam]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of team results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(resource=ComicvineResource.TEAM, query=query, max_results=max_results)

    def list_locations(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicLocation]:
        """Request a list of Locations.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Location objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.LOCATION, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.LOCATION, id_=location_id)

    def search_locations(self, query: str, max_results: int | None = 500) -> list[BasicLocation]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of location results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(
            resource=ComicvineResource.LOCATION, query=query, max_results=max_results
        )

    def list_concepts(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicConcept]:
        """Request a list of Concepts.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Concept objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.CONCEPT, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.CONCEPT, id_=concept_id)

    def search_concepts(self, query: str, max_results: int | None = 500) -> list[BasicConcept]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of concept results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(
            resource=ComicvineResource.CONCEPT, query=query, max_results=max_results
        )

    def list_powers(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicPower]:
        """Request a list of Powers.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Power objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.POWER, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.POWER, id_=power_id)

    def search_powers(self, query: str, max_results: int | None = 500) -> list[BasicPower]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of power results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(resource=ComicvineResource.POWER, query=query, max_results=max_results)

    def list_origins(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicOrigin]:
        """Request a list of Origins.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Origin objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.ORIGIN, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.ORIGIN, id_=origin_id)

    def search_origins(self, query: str, max_results: int | None = 500) -> list[BasicOrigin]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of origin results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(resource=ComicvineResource.ORIGIN, query=query, max_results=max_results)

    def list_items(
        self, params: dict[str, Any] | None = None, max_results: int | None = 500
    ) -> list[BasicItem]:
        """Request a list of Items.

        Args:
            params: Parameters to add to the request.
            max_results: If given, return at most this many results.

        Returns:
            A list of Item objects.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._get_list(
            resource=ComicvineResource.ITEM, params=params, max_results=max_results
        )

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
        return self._get_item(resource=ComicvineResource.ITEM, id_=item_id)

    def search_items(self, query: str, max_results: int | None = 500) -> list[BasicItem]:
        """Request a list of search results.

        Args:
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of item results.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(resource=ComicvineResource.ITEM, query=query, max_results=max_results)

    @deprecated("Use the resource specific search functions instead.")
    def search(
        self, resource: ComicvineResource, query: str, max_results: int | None = 500
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

        **Deprecated:** Use the resource specific search functions instead.

        Args:
            resource: Filter which type of resource to return.
            query: Search query string.
            max_results: If given, return at most this many results.

        Returns:
            A list of results, mapped to the given resource.

        Raises:
            ServiceError: If the API response is invalid or validation fails.
            AuthenticationError: If credentials are invalid.
            RateLimitError: If the API rate limit is exceeded.
        """
        return self._search(resource=resource, query=query, max_results=max_results)
