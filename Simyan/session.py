"""
Session module.

This module provides the following classes:

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


class CVType(Enum):
    """Class for Comic Vine resource ids."""

    PUBLISHER = 4010
    VOLUME = 4050
    ISSUE = 4000
    STORY_ARC = 4045
    CREATOR = 4040

    def __str__(self):
        """Return string for Comic Vine resouce id."""
        return f"{self.value}"


class Session:
    """
    Session to request api endpoints.

    :param str api_key: The api key used for authentication with Comic Vine
    :param SqliteCache, optional: SqliteCache to use
    """

    def __init__(self, api_key: str, cache: Optional[SqliteCache] = None):
        """Intialize a new Session."""
        self.api_key = api_key
        self.header = {"User-Agent": f"Simyan/{platform.system()}: {platform.release()}"}
        self.api_url = "https://comicvine.gamespot.com/api/{}/"
        self.cache = cache

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def call(self, endpoint: List[Union[str, int]], params: Dict[str, Union[str, int]] = None) -> Dict[str, Any]:
        """
        Make request for api endpoints.

        :param list[str, int] endpoint: The endpoint to request information from.
        :param dict params: Parameters to add to the request.
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
        Request data for a publisher based on its ``_id``.

        :param int _id: The publisher id.

        :return: :class:`Publisher` object
        :rtype: Publisher
        """
        try:
            return PublisherSchema().load(self.call(["publisher", f"{CVType.PUBLISHER}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def publisher_list(self, params: Dict[str, Union[str, int]] = None) -> PublisherList:
        """
        Request a list of publishers.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`PublisherResult` objects.
        :rtype: PublishersList
        """
        results = self._retrieve_all_responses("publishers", params)
        return PublisherList(results)

    def volume(self, _id: int) -> Volume:
        """
        Request data for a volume based on its ``_id``.

        :param int _id: The volume id.

        :return: :class:`Volume` object
        :rtype: Volume
        """
        try:
            return VolumeSchema().load(self.call(["volume", f"{CVType.VOLUME}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def volume_list(self, params: Dict[str, Union[str, int]] = None) -> VolumeList:
        """
        Request a list of volumes.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`Volumeresult` objects.
        :rtype: VolumeList
        """
        results = self._retrieve_all_responses("volumes", params)
        return VolumeList(results)

    def issue(self, _id: int) -> Issue:
        """
        Request data for an issue based on it's ``_id``.

        :param int _id: The issue id.

        :return: :class:`Issue` object
        :rtype: Issue
        """
        try:
            return IssueSchema().load(self.call(["issue", f"{CVType.ISSUE}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def issue_list(self, params: Dict[str, Union[str, int]] = None) -> IssueList:
        """
        Request a list of issues.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`IssueResult` objects.
        :rtype: IssuesList
        """
        results = self._retrieve_all_responses("issues", params)
        return IssueList(results)

    def story_arc(self, _id: int) -> StoryArc:
        """
        Request data for a story arc based on its ``_id``.

        :param int _id: The story arc id.

        :return: :class:`StoryArc` object
        :rtype: StoryArc
        """
        try:
            return StoryArcSchema().load(self.call(["story_arc", f"{CVType.STORY_ARC}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def story_arc_list(self, params: Dict[str, Union[str, int]] = None) -> StoryArcList:
        """
        Request a list of story arc.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`StoryArcResult` objects.
        :rtype: StoryArcList
        """
        results = self._retrieve_all_responses("story_arcs", params)
        return StoryArcList(results)

    def creator(self, _id: int) -> Creator:
        """
        Request data for a creator based on its ``_id``.

        :param int _id: The creator id.

        :return: :class:`Creator` object
        :rtype: Creator
        """
        try:
            return CreatorSchema().load(self.call(["person", f"{CVType.CREATOR}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def creator_list(self, params: Dict[str, Union[str, int]] = None) -> CreatorList:
        """
        Request a list of creators.

        :param params: Parameters to add to the request.
        :type params: dict, optional

        :return: A list of :class:`CreatorResult` objects.
        :rtype: CreatorsList
        """
        results = self._retrieve_all_responses("people", params)
        return CreatorList(results)

    def _retrieve_all_responses(self, resource: str, params: Dict[str, Union[str, int]] = None):
        if params is None:
            params = {}
        response = self.call([resource], params=params)
        result = response["results"]
        while response["number_of_total_results"] > response["offset"] + response["number_of_page_results"]:
            params["offset"] = response["offset"] + response["number_of_page_results"]
            response = self.call([resource], params=params)
            result.extend(response["results"])
        return result
