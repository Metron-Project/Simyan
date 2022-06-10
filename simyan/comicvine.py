"""
The Comicvine module.

This module provides the following classes:

- ComicvineResource
- Comicvine
"""
import platform
import re
from collections import OrderedDict
from enum import Enum
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from marshmallow import ValidationError
from ratelimit import limits, sleep_and_retry
from requests import get
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout

from simyan import __version__
from simyan.exceptions import APIError, AuthenticationError, CacheError
from simyan.schemas.character import Character, CharacterResult
from simyan.schemas.creator import Creator, CreatorResult, pre_process_creator
from simyan.schemas.issue import Issue, IssueResult
from simyan.schemas.publisher import Publisher, PublisherResult
from simyan.schemas.story_arc import StoryArc, StoryArcResult
from simyan.schemas.volume import Volume, VolumeResult, pre_process_volume
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
            APIError: If there is an issue with the request or response from the Comicvine API.
        """
        if params is None:
            params = {}

        try:
            response = get(url, params=params, headers=self.headers, timeout=self.timeout)
            return response.json()
        except ConnectionError as ce:
            raise APIError(f"Unable to connect to `{url}`: {ce}")
        except HTTPError as he:
            raise APIError(he.response.text)
        except ReadTimeout:
            raise APIError("Server took too long to respond")
        except JSONDecodeError as de:
            raise APIError(f"Invalid response from `{url}`: {de}")

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
            APIError: If there is an issue with the request or response from the Comicvine API.
            AuthenticationError: If Comicvine returns with an invalid API key response.
            CacheError: If it is unable to retrieve or push to the Cache correctly.
        """
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        params["format"] = "json"

        cache_params = ""
        if params:
            ordered_params = OrderedDict(sorted(params.items(), key=lambda x: x[0]))
            cache_params = f"?{urlencode(ordered_params)}"

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
            if response["error"] == "Invalid API Key":
                raise AuthenticationError(response["error"])
            raise APIError(response["error"])

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
            APIError: If there is an issue with mapping the response to the Publisher object.
        """
        try:
            result = self._get_request(
                endpoint=f"/publisher/{ComicvineResource.PUBLISHER}-{publisher_id}"
            )["results"]
            return Publisher.schema().load(result)
        except ValidationError as error:
            raise APIError(error.messages)

    def publisher_list(self, params: Optional[Dict[str, Any]] = None) -> List[PublisherResult]:
        """
        Request data for a list of Publishers.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of PublisherResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the PublisherList object.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/publishers", params=params)
            return PublisherResult.schema().load(results, many=True)
        except ValidationError as error:
            raise APIError(error.messages)

    def volume(self, volume_id: int) -> Volume:
        """
        Request data for a Volume based on its id.

        Args:
            volume_id: The Volume id.
        Returns:
            A Volume object
        Raises:
            APIError: If there is an issue with mapping the response to the Volume object.
        """
        try:
            result = self._get_request(endpoint=f"/volume/{ComicvineResource.VOLUME}-{volume_id}")[
                "results"
            ]
            return Volume.schema().load(pre_process_volume(result))
        except ValidationError as error:
            raise APIError(error.messages)

    def volume_list(
        self, params: Optional[Dict[str, Union[str, int]]] = None
    ) -> List[VolumeResult]:
        """
        Request data for a list of Volumes.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of VolumeResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the VolumeList object.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/volumes", params=params)
            return VolumeResult.schema().load([pre_process_volume(x) for x in results], many=True)
        except ValidationError as error:
            raise APIError(error.messages)

    def issue(self, issue_id: int) -> Issue:
        """
        Request data for an Issue based on its id.

        Args:
            issue_id: The Issue id.
        Returns:
            A Issue object
        Raises:
            APIError: If there is an issue with mapping the response to the Issue object.
        """
        try:
            result = self._get_request(endpoint=f"/issue/{ComicvineResource.ISSUE}-{issue_id}")[
                "results"
            ]
            return Issue.schema().load(result)
        except ValidationError as error:
            raise APIError(error.messages)

    def issue_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> List[IssueResult]:
        """
        Request data for a list of Issues.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of IssueResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the IssueList object.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/issues", params=params)
            return IssueResult.schema().load(results, many=True)
        except ValidationError as error:
            raise APIError(error.messages)

    def story_arc(self, story_arc_id: int) -> StoryArc:
        """
        Request data for a Story Arc based on its id.

        Args:
            story_arc_id: The StoryArc id.
        Returns:
            A StoryArc object
        Raises:
            APIError: If there is an issue with mapping the response to the StoryArc object.
        """
        try:
            result = self._get_request(
                endpoint=f"/story_arc/{ComicvineResource.STORY_ARC}-{story_arc_id}"
            )["results"]
            return StoryArc.schema().load(result)
        except ValidationError as error:
            raise APIError(error.messages)

    def story_arc_list(
        self, params: Optional[Dict[str, Union[str, int]]] = None
    ) -> List[StoryArcResult]:
        """
        Request data for a list of Story Arcs.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of StoryArcResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the StoryArcList object.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/story_arcs", params=params)
            return StoryArcResult.schema().load(results, many=True)
        except ValidationError as error:
            raise APIError(error.messages)

    def creator(self, creator_id: int) -> Creator:
        """
        Request data for a Creator based on its id.

        Args:
            creator_id: The Creator id.
        Returns:
            A Creator object
        Raises:
            APIError: If there is an issue with mapping the response to the Creator object.
        """
        try:
            result = self._get_request(
                endpoint=f"/person/{ComicvineResource.CREATOR}-{creator_id}"
            )["results"]
            # print(pre_process_creator(result))
            return Creator.schema().load(pre_process_creator(result))
        except ValidationError as error:
            raise APIError(error.messages)

    def creator_list(
        self, params: Optional[Dict[str, Union[str, int]]] = None
    ) -> List[CreatorResult]:
        """
        Request data for a list of Creators.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of CreatorResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the CreatorList object.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/people", params=params)
            return CreatorResult.schema().load([pre_process_creator(x) for x in results], many=True)
        except ValidationError as error:
            raise APIError(error.messages)

    def character(self, character_id: int) -> Character:
        """
        Request data for a Character based on its id.

        Args:
            character_id: The Character id.
        Returns:
            A Character object
        Raises:
            APIError: If there is an issue with mapping the response to the Character object.
        """
        try:
            result = self._get_request(
                endpoint=f"/character/{ComicvineResource.CHARACTER}-{character_id}"
            )["results"]
            return Character.schema().load(result)
        except ValidationError as error:
            raise APIError(error.messages)

    def character_list(
        self, params: Optional[Dict[str, Union[str, int]]] = None
    ) -> List[CharacterResult]:
        """
        Request data for a list of Characters.

        Args:
            params: Parameters to add to the request.
        Returns:
            A list of CharacterResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the CharacterList object.
        """
        try:
            results = self._retrieve_all_responses(endpoint="/characters", params=params)
            return CharacterResult.schema().load(results, many=True)
        except ValidationError as error:
            raise APIError(error.messages)

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
        result = response["results"]
        while (
            response["number_of_total_results"]
            > response["offset"] + response["number_of_page_results"]
        ):
            params["offset"] = response["offset"] + response["number_of_page_results"]
            response = self._get_request(endpoint=endpoint, params=params)
            result.extend(response["results"])
        return result
