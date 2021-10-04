"""
Session module.

This module provides the following classes:

- Session
- CVType
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
from requests.exceptions import ConnectionError

from Simyan.character import Character, CharacterSchema
from Simyan.character_list import CharacterList
from Simyan.creator import Creator, CreatorSchema
from Simyan.creator_list import CreatorList
from Simyan.exceptions import APIError, CacheError
from Simyan.issue import Issue, IssueSchema
from Simyan.issue_list import IssueList
from Simyan.publisher import Publisher, PublisherSchema
from Simyan.publisher_list import PublisherList
from Simyan.sqlite_cache import SqliteCache
from Simyan.story_arc import StoryArc, StoryArcSchema
from Simyan.story_arc_list import StoryArcList
from Simyan.volume import Volume, VolumeSchema
from Simyan.volume_list import VolumeList

MINUTE = 60


class ComicVineResource(Enum):
    """Class for ComicVine Resource ids."""

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
            String version of the ComicVineResource value
        """
        return f"{self.value}"


class Session:
    """
    Session to request ComicVine API endpoints.

    Args:
        api_key: User's API key to access the ComicVine API.
        cache: SqliteCache to use if set.

    Attributes:
        api_key (str): User's API key to access the ComicVine API.
        header (dict of str: str): Header that will be used when accessing the ComicVine API.
        api_url (str): Url of the ComicVine API.
        cache (SqliteCache, Optional): SqliteCache to use if set.
    """

    def __init__(self, api_key: str, cache: Optional[SqliteCache] = None):
        self.api_key = api_key
        self.header = {"User-Agent": f"Simyan/{platform.system()}: {platform.release()}"}
        self.api_url = "https://comicvine.gamespot.com/api/{}/"
        self.cache = cache

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _get(self, endpoint: List[Union[str, int]], params: Dict[str, Union[str, int]] = None) -> dict[str, Any]:
        """
        Make GET request to ComicVine API endpoint.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.

        Returns:
            Json response from the ComicVine API.

        Raises:
            CacheError: If is unable to retrieve or push to the Cache correctly.
            APIError: If there is an issue with the request or response to the ComicVine API.
        """
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        params["format"] = "json"

        cache_params = ""
        if params:
            ordered_params = OrderedDict(sorted(params.items(), key=lambda x: x[0]))
            cache_params = f"?{urlencode(ordered_params)}"

        url = self.api_url.format("/".join(str(e) for e in endpoint))
        cache_key = f"{url}{cache_params}"
        cache_key = re.sub(r"(.+api_key=)(.+?)(&.+)", r"\1*****\3", cache_key)

        if self.cache:
            try:
                cached_response = self.cache.get(cache_key)
                if cached_response is not None:
                    return cached_response
            except AttributeError as e:
                raise CacheError(f"Cache object passed in is missing attribute: {repr(e)}")

        try:
            response = get(url, params=params, headers=self.header)
        except ConnectionError as e:
            raise APIError(f"Connection error: {repr(e)}")

        try:
            data = response.json()
        except JSONDecodeError as e:
            raise APIError(f"Invalid request: {repr(e)}")

        if "error" in data and data["error"] != "OK":
            raise APIError(data["error"])
        if self.cache:
            try:
                self.cache.insert(cache_key, data)
            except AttributeError as e:
                raise CacheError(f"Cache object passed in is missing attribute: {repr(e)}")

        return data

    def publisher(self, _id: int) -> Publisher:
        """
        Request data for a Publisher based on its ``_id``.

        Args:
            _id: The Publisher id.

        Returns:
            A `Publisher` object

        Raises:
            APIError: If there is an issue with the mapping the response to the Publisher Object.
        """
        try:
            return PublisherSchema().load(self._get(["publisher", f"{ComicVineResource.PUBLISHER}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def publisher_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> PublisherList:
        """
        Request data for a list of Publishers.

        Args:
            params: Parameters to add to the request.

        Returns:
            A list of `PublisherResult` objects.

        Raises:
            APIError: If there is an issue with the mapping the response to the PublisherList Object.
        """
        results = self._retrieve_all_responses(["publishers"], params)
        return PublisherList(results)

    def volume(self, _id: int) -> Volume:
        """
        Request data for a Volume based on its ``_id``.

        Args:
            _id: The Volume id.

        Returns:
            A `Volume` object

        Raises:
            APIError: If there is an issue with the mapping the response to the Volume Object.
        """
        try:
            return VolumeSchema().load(self._get(["volume", f"{ComicVineResource.VOLUME}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def volume_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> VolumeList:
        """
        Request data for a list of Volumes.

        Args:
            params: Parameters to add to the request.

        Returns:
            A list of `VolumeResult` objects.

        Raises:
            APIError: If there is an issue with the mapping the response to the VolumeList Object.
        """
        results = self._retrieve_all_responses(["volumes"], params)
        return VolumeList(results)

    def issue(self, _id: int) -> Issue:
        """
        Request data for an Issue based on its ``_id``.

        Args:
            _id: The Issue id.

        Returns:
            A `Issue` object

        Raises:
            APIError: If there is an issue with the mapping the response to the Issue Object.
        """
        try:
            return IssueSchema().load(self._get(["issue", f"{ComicVineResource.ISSUE}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def issue_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> IssueList:
        """
        Request data for a list of Issues.

        Args:
            params: Parameters to add to the request.

        Returns:
            A list of `IssueResult` objects.

        Raises:
            APIError: If there is an issue with the mapping the response to the IssueList Object.
        """
        results = self._retrieve_all_responses(["issues"], params)
        return IssueList(results)

    def story_arc(self, _id: int) -> StoryArc:
        """
        Request data for a Story Arc based on its ``_id``.

        Args:
            _id: The Story Arc id.

        Returns:
            A `StoryArc` object

        Raises:
            APIError: If there is an issue with the mapping the response to the StoryArc Object.
        """
        try:
            return StoryArcSchema().load(self._get(["story_arc", f"{ComicVineResource.STORY_ARC}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def story_arc_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> StoryArcList:
        """
        Request data for a list of Story Arcs.

        Args:
            params: Parameters to add to the request.

        Returns:
            A list of `StoryArcResult` objects.

        Raises:
            APIError: If there is an issue with the mapping the response to the StoryArcList Object.
        """
        results = self._retrieve_all_responses(["story_arcs"], params)
        return StoryArcList(results)

    def creator(self, _id: int) -> Creator:
        """
        Request data for a Creator based on its ``_id``.

        Args:
            _id: The Creator id.

        Returns:
            A `Creator` object

        Raises:
            APIError: If there is an issue with the mapping the response to the Creator Object.
        """
        try:
            return CreatorSchema().load(self._get(["person", f"{ComicVineResource.CREATOR}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def creator_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> CreatorList:
        """
        Request data for a list of Creators.

        Args:
            params: Parameters to add to the request.

        Returns:
            A list of `CreatorResult` objects.

        Raises:
            APIError: If there is an issue with the mapping the response to the CreatorList Object.
        """
        results = self._retrieve_all_responses(["people"], params)
        return CreatorList(results)

    def character(self, _id: int) -> Character:
        """
        Request data for a Character based on its ``_id``.

        Args:
            _id: The Character id.

        Returns:
            A `Character` object

        Raises:
            APIError: If there is an issue with the mapping the response to the Character Object.
        """
        try:
            return CharacterSchema().load(self._get(["character", f"{ComicVineResource.CHARACTER}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def character_list(self, params: Optional[Dict[str, Union[str, int]]] = None) -> CharacterList:
        """
        Request data for a list of Characters.

        Args:
            params: Parameters to add to the request.

        Returns:
            A list of `CharacterResult` objects.

        Raises:
            APIError: If there is an issue with the mapping the response to the CharacterList Object.
        """
        results = self._retrieve_all_responses(["characters"], params)
        return CharacterList(results)

    def _retrieve_all_responses(
        self, endpoint: List[Union[str, int]], params: Optional[Dict[str, Union[str, int]]] = None
    ) -> list[dict[str, Any]]:
        """
        Keep getting responses until all the results are collected.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.

        Returns:
            A list of json response results.
        """
        if params is None:
            params = {}
        response = self._get(endpoint=endpoint, params=params)
        result = response["results"]
        while response["number_of_total_results"] > response["offset"] + response["number_of_page_results"]:
            params["offset"] = response["offset"] + response["number_of_page_results"]
            response = self._get(endpoint=endpoint, params=params)
            result.extend(response["results"])
        return result
