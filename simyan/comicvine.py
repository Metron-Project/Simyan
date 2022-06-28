"""
The Comicvine module.

This module provides the following classes:

- ComicvineResource
- Comicvine
"""
import platform
import re
from enum import Enum
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import ValidationError, parse_obj_as
from ratelimit import limits, sleep_and_retry
from requests import get
from requests.exceptions import ConnectionError, HTTPError

from simyan import __version__
from simyan.exceptions import AuthenticationError, CacheError, ServiceError
from simyan.resource_type import ResourceType
from simyan.schemas.character import Character
from simyan.schemas.creator import Creator
from simyan.schemas.issue import Issue
from simyan.schemas.publisher import Publisher
from simyan.schemas.story_arc import StoryArc
from simyan.schemas.volume import Volume
from simyan.sqlite_cache import SQLiteCache

MINUTE = 60


class ComicvineResource(Enum):
    """Class for Comicvine Resource ids."""

    PUBLISHER = 4010
    VOLUME = 4050
    ISSUE = 4000
    STORY_ARC = 4045
    CREATOR = 4040
    CHARACTER = 4005

    def __str__(self):
        """
        Generate string version of Resource id.

        Returns:
            String version of the ComicvineResource id.
        """
        return f"{self.value}"


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
        except ConnectionError:
            raise ServiceError(f"Unable to connect to `{url}`")
        except HTTPError as err:
            if err.response.status_code == 401:
                raise AuthenticationError("Invalid API Key")
            elif err.response.status_code == 404:
                raise ServiceError("Unknown endpoint")
            raise ServiceError(err.response.json()["error"])
        except JSONDecodeError:
            raise ServiceError(f"Unable to parse response from `{url}` as Json")

    def _get_request(
        self, endpoint: str, params: Dict[str, str] = None, skip_cache: bool = False
    ) -> Dict[str, Any]:
        """
        Check cache or make GET request to Comicvine API endpoint.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.
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

        cache_params = ""
        if params:
            cache_params = f"?{urlencode({k: params[k] for k in sorted(params)})}"

        url = self.API_URL + endpoint
        cache_key = f"{url}{cache_params}"
        cache_key = re.sub(r"(.+api_key=)(.+?)(&.+)", r"\1*****\3", cache_key)

        if self.cache and not skip_cache:
            try:
                cached_response = self.cache.get(cache_key)
                if cached_response is not None:
                    return cached_response
            except AttributeError as e:
                raise CacheError(f"Cache object passed in is missing attribute: {repr(e)}")

        response = self._perform_get_request(url=url, params=params)
        if "error" in response and response["error"] != "OK":
            raise ServiceError(response["error"])

        if self.cache and not skip_cache:
            try:
                self.cache.insert(cache_key, response)
            except AttributeError as e:
                raise CacheError(f"Cache object passed in is missing attribute: {repr(e)}")

        return response

    def publisher(self, publisher_id: int) -> Publisher:
        """
        Request data for a Publisher based on its id.

        Args:
            publisher_id: The Publisher id.
        Returns:
            A Publisher object
        Raises:
            ServiceError: If there is an issue with mapping the response to the Publisher object.
        """
        try:
            result = self._get_request(
                endpoint=f"/publisher/{ComicvineResource.PUBLISHER}-{publisher_id}"
            )["results"]
            return parse_obj_as(Publisher, result)
        except ValidationError as err:
            raise ServiceError(err)

    def publisher_list(self, params: Optional[Dict[str, Any]] = None) -> List[Publisher]:
        """
        Request data for a list of Publishers.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of Publisher objects.
        Raises:
            ServiceError: If there is an issue with mapping the response to a List of Publisher objects.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/publishers/", params=params)
            return parse_obj_as(List[Publisher], results)
        except ValidationError as err:
            raise ServiceError(err)

    def volume(self, volume_id: int) -> Volume:
        """
        Request data for a Volume based on its id.

        Args:
            volume_id: The Volume id.
        Returns:
            A Volume object
        Raises:
            ServiceError: If there is an issue with mapping the response to the Volume object.
        """
        try:
            result = self._get_request(endpoint=f"/volume/{ComicvineResource.VOLUME}-{volume_id}")[
                "results"
            ]
            return parse_obj_as(Volume, result)
        except ValidationError as err:
            raise ServiceError(err)

    def volume_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> List[Volume]:
        """
        Request data for a list of Volumes.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of VolumeResult objects.
        Raises:
            ServiceError: If there is an issue with mapping the response to a List of Volume objects.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/volumes/", params=params)
            return parse_obj_as(List[Volume], results)
        except ValidationError as err:
            raise ServiceError(err)

    def issue(self, issue_id: int) -> Issue:
        """
        Request data for an Issue based on its id.

        Args:
            issue_id: The Issue id.
        Returns:
            A Issue object
        Raises:
            ServiceError: If there is an issue with mapping the response to the Issue object.
        """
        try:
            result = self._get_request(endpoint=f"/issue/{ComicvineResource.ISSUE}-{issue_id}")[
                "results"
            ]
            return parse_obj_as(Issue, result)
        except ValidationError as err:
            raise ServiceError(err)

    def issue_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> List[Issue]:
        """
        Request data for a list of Issues.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of IssueResult objects.
        Raises:
            ServiceError: If there is an issue with mapping the response to a List of Issue objects.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/issues/", params=params)
            return parse_obj_as(List[Issue], results)
        except ValidationError as err:
            raise ServiceError(err)

    def story_arc(self, story_arc_id: int) -> StoryArc:
        """
        Request data for a Story Arc based on its id.

        Args:
            story_arc_id: The StoryArc id.
        Returns:
            A StoryArc object
        Raises:
            ServiceError: If there is an issue with mapping the response to the StoryArc object.
        """
        try:
            result = self._get_request(
                endpoint=f"/story_arc/{ComicvineResource.STORY_ARC}-{story_arc_id}"
            )["results"]
            return parse_obj_as(StoryArc, result)
        except ValidationError as err:
            raise ServiceError(err)

    def story_arc_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> List[StoryArc]:
        """
        Request data for a list of Story Arcs.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of StoryArcResult objects.
        Raises:
            ServiceError: If there is an issue with mapping the response to a List of StoryArc objects.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/story_arcs/", params=params)
            return parse_obj_as(List[StoryArc], results)
        except ValidationError as err:
            raise ServiceError(err)

    def creator(self, creator_id: int) -> Creator:
        """
        Request data for a Creator based on its id.

        Args:
            creator_id: The Creator id.
        Returns:
            A Creator object
        Raises:
            ServiceError: If there is an issue with mapping the response to the Creator object.
        """
        try:
            result = self._get_request(
                endpoint=f"/person/{ComicvineResource.CREATOR}-{creator_id}"
            )["results"]
            return parse_obj_as(Creator, result)
        except ValidationError as err:
            raise ServiceError(err)

    def creator_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> List[Creator]:
        """
        Request data for a list of Creators.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of CreatorResult objects.
        Raises:
            ServiceError: If there is an issue with mapping the response to a List of Creator objects.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/people/", params=params)
            return parse_obj_as(List[Creator], results)
        except ValidationError as err:
            raise ServiceError(err)

    def character(self, character_id: int) -> Character:
        """
        Request data for a Character based on its id.

        Args:
            character_id: The Character id.
        Returns:
            A Character object
        Raises:
            ServiceError: If there is an issue with mapping the response to the Character object.
        """
        try:
            result = self._get_request(
                endpoint=f"/character/{ComicvineResource.CHARACTER}-{character_id}"
            )["results"]
            return parse_obj_as(Character, result)
        except ValidationError as err:
            raise ServiceError(err)

    def character_list(
        self, params: Optional[Dict[str, Union[str, int]]] = None
    ) -> List[Character]:
        """
        Request data for a list of Characters.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of CharacterResult objects.
        Raises:
            ServiceError: If there is an issue with mapping the response to a List of Character objects.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/characters/", params=params)
            return parse_obj_as(List[Character], results)
        except ValidationError as err:
            raise ServiceError(err)

    def search(
        self, resource: ResourceType, query: str
    ) -> Union[List[Character], List[Issue], List[Volume], List[Creator]]:
        params = {"query": query, "resources": resource.value[0], "page": 1}
        response = self._get_request(endpoint="/search/", params=params)
        results = response["results"]
        while response["results"] and len(results) < response["number_of_total_results"]:
            params["page"] += 1
            response = self._get_request(endpoint="/search/", params=params)
            results.extend(response["results"])
        try:
            return parse_obj_as(resource.value[1], results)
        except ValidationError as err:
            raise ServiceError(err)

    def _retrieve_all_responses(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get responses until all the results are collected.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.
        Returns:
            A list of Json response results.
        """
        if params is None:
            params = {}
        response = self._get_request(endpoint=endpoint, params=params)
        results = response["results"]
        while response["results"] and len(results) < response["number_of_total_results"]:
            params["offset"] = len(results)
            response = self._get_request(endpoint=endpoint, params=params)
            results.extend(response["results"])
        return results
