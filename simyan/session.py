"""
The Session module.

This module provides the following classes:

- ComicVineResource
- Session
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

from simyan import __version__
from simyan.character import Character, CharacterSchema
from simyan.character_list import CharacterList
from simyan.creator import Creator, CreatorSchema
from simyan.creator_list import CreatorList
from simyan.exceptions import APIError, AuthenticationError, CacheError
from simyan.issue import Issue, IssueSchema
from simyan.issue_list import IssueList
from simyan.publisher import Publisher, PublisherSchema
from simyan.publisher_list import PublisherList
from simyan.sqlite_cache import SQLiteCache
from simyan.story_arc import StoryArc, StoryArcSchema
from simyan.story_arc_list import StoryArcList
from simyan.volume import Volume, VolumeSchema
from simyan.volume_list import VolumeList

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
            String version of the ComicVineResource id.
        """
        return f"{self.value}"


class Session:
    """
    Session to request ComicVine API endpoints.

    Args:
        api_key: User's API key to access the ComicVine API.
        cache: SQLiteCache to use if set.

    Attributes:
        api_key (str): User's API key to access the ComicVine API.
        header (Dict[str, str]): Header used when requesting from ComicVine API.
        api_url (str): ComicVine API url.
        cache (Optional[SQLiteCache]): SQLiteCache to use if set.
    """

    def __init__(self, api_key: str, cache: Optional[SQLiteCache] = None):
        self.api_key = api_key
        self.header = {"User-Agent": f"Simyan/{__version__}/{platform.system()}: {platform.release()}"}
        self.api_url = "https://comicvine.gamespot.com/api/{}/"
        self.cache = cache

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def _get(self, endpoint: List[Union[str, int]], params: Dict[str, Union[str, int]] = None) -> Dict[str, Any]:
        """
        Make GET request to ComicVine API endpoint.

        Args:
            endpoint: The endpoint to request information from.
            params: Parameters to add to the request.
        Returns:
            Json response from the ComicVine API.
        Raises:
            APIError: If there is an issue with the request or response from the ComicVine API.
            AuthenticationError: If Comicvine returns with an invalid API key response..
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
            if data["error"] == "Invalid API Key":
                raise AuthenticationError(data["error"])
            raise APIError(data["error"])
        if self.cache:
            try:
                self.cache.insert(cache_key, data)
            except AttributeError as e:
                raise CacheError(f"Cache object passed in is missing attribute: {repr(e)}")

        return data

    def publisher(self, _id: int) -> Publisher:
        """
        Request data for a Publisher based on its id.

        Args:
            _id: The Publisher id.
        Returns:
            A Publisher object
        Raises:
            APIError: If there is an issue with mapping the response to the Publisher object.
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
            A list of PublisherResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the PublisherList object.
        """
        results = self._retrieve_all_responses(["publishers"], params)
        return PublisherList(results)

    def volume(self, _id: int) -> Volume:
        """
        Request data for a Volume based on its id.

        Args:
            _id: The Volume id.
        Returns:
            A Volume object
        Raises:
            APIError: If there is an issue with mapping the response to the Volume object.
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
            A list of VolumeResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the VolumeList object.
        """
        results = self._retrieve_all_responses(["volumes"], params)
        return VolumeList(results)

    def issue(self, _id: int) -> Issue:
        """
        Request data for an Issue based on its id.

        Args:
            _id: The Issue id.
        Returns:
            A Issue object
        Raises:
            APIError: If there is an issue with mapping the response to the Issue object.
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
            A list of IssueResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the IssueList object.
        """
        results = self._retrieve_all_responses(["issues"], params)
        return IssueList(results)

    def story_arc(self, _id: int) -> StoryArc:
        """
        Request data for a Story Arc based on its id.

        Args:
            _id: The StoryArc id.
        Returns:
            A StoryArc object
        Raises:
            APIError: If there is an issue with mapping the response to the StoryArc object.
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
            A list of StoryArcResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the StoryArcList object.
        """
        results = self._retrieve_all_responses(["story_arcs"], params)
        return StoryArcList(results)

    def creator(self, _id: int) -> Creator:
        """
        Request data for a Creator based on its id.

        Args:
            _id: The Creator id.
        Returns:
            A Creator object
        Raises:
            APIError: If there is an issue with mapping the response to the Creator object.
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
            A list of CreatorResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the CreatorList object.
        """
        results = self._retrieve_all_responses(["people"], params)
        return CreatorList(results)

    def character(self, _id: int) -> Character:
        """
        Request data for a Character based on its id.

        Args:
            _id: The Character id.
        Returns:
            A Character object
        Raises:
            APIError: If there is an issue with mapping the response to the Character object.
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
            A list of CharacterResult objects.
        Raises:
            APIError: If there is an issue with mapping the response to the CharacterList object.
        """
        results = self._retrieve_all_responses(["characters"], params)
        return CharacterList(results)

    def _retrieve_all_responses(
        self, endpoint: List[Union[str, int]], params: Optional[Dict[str, Union[str, int]]] = None
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
        response = self._get(endpoint=endpoint, params=params)
        result = response["results"]
        while response["number_of_total_results"] > response["offset"] + response["number_of_page_results"]:
            params["offset"] = response["offset"] + response["number_of_page_results"]
            response = self._get(endpoint=endpoint, params=params)
            result.extend(response["results"])
        return result
