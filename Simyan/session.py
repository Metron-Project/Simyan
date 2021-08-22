import platform
import re
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode
from json import JSONDecodeError

from marshmallow import ValidationError
from ratelimit import limits, sleep_and_retry
from requests import get
from requests.exceptions import ConnectionError

from .exceptions import CacheError, APIError
from .issue import Issue, IssueSchema, IssueList
from .publisher import Publisher, PublisherSchema, PublisherList
from .sqlite_cache import SqliteCache
from .volume import Volume, VolumeSchema, VolumeList

MINUTE = 60


class Session:
    def __init__(self, api_key: str, cache: Optional[SqliteCache] = None):
        self.api_key = api_key
        self.header = {
            'User-Agent': f"Simyan/{platform.system()}: {platform.release()}"
        }
        self.api_url = 'https://comicvine.gamespot.com/api/{}/'
        self.cache = cache

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def call(self, endpoint: List[Union[str, int]], params: Dict[str, Union[str, int]] = None) -> Dict[str, Any]:
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        params['format'] = 'json'

        cache_params = ""
        if params:
            ordered_params = OrderedDict(sorted(params.items(), key=lambda x: x[0]))
            cache_params = "?{}".format(urlencode(ordered_params))

        url = self.api_url.format('/'.join(str(e) for e in endpoint))
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

        if 'error' in data and data['error'] != 'OK':
            raise APIError(data['error'])
        if self.cache:
            try:
                self.cache.insert(cache_key, data)
            except AttributeError as e:
                raise CacheError(f"Cache object passed in is missing attribute: {repr(e)}")

        return data

    def publisher(self, _id: int) -> Publisher:
        try:
            return PublisherSchema().load(self.call(["publisher", f"4010-{_id}"])['results'])
        except ValidationError as error:
            raise APIError(error.messages)

    def publisher_list(self, params: Dict[str, Union[str, int]] = None) -> PublisherList:
        if params is None:
            params = {}
        response = self.call(["publishers"], params=params)
        results = response['results']
        while response['number_of_total_results'] > response['offset'] + response['number_of_page_results']:
            params['offset'] = response['offset'] + response['number_of_page_results']
            response = self.call(["publishers"], params=params)
            results.extend(response['results'])
        return PublisherList(results)

    def volume(self, _id: int) -> Volume:
        try:
            return VolumeSchema().load(self.call(["volume", f"4050-{_id}"])['results'])
        except ValidationError as error:
            raise APIError(error.messages)

    def volume_list(self, params: Dict[str, Union[str, int]] = None) -> VolumeList:
        if params is None:
            params = {}
        response = self.call(["volumes"], params=params)
        results = response['results']
        while response['number_of_total_results'] > response['offset'] + response['number_of_page_results']:
            params['offset'] = response['offset'] + response['number_of_page_results']
            response = self.call(["volumes"], params=params)
            results.extend(response['results'])
        return VolumeList(results)

    def issue(self, _id: int) -> Issue:
        try:
            return IssueSchema().load(self.call(["issue", f"4000-{_id}"])['results'])
        except ValidationError as error:
            raise APIError(error.messages)

    def issue_list(self, params: Dict[str, Union[str, int]] = None) -> IssueList:
        if params is None:
            params = {}
        response = self.call(["issues"], params=params)
        results = response['results']
        while response['number_of_total_results'] > response['offset'] + response['number_of_page_results']:
            params['offset'] = response['offset'] + response['number_of_page_results']
            response = self.call(["issues"], params=params)
            results.extend(response['results'])
        return IssueList(results)
