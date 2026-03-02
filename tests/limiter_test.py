from datetime import timedelta
from pathlib import Path
from typing import Final
from unittest.mock import patch

import pytest
from freezegun.api import FrozenDateTimeFactory
from pyrate_limiter import Duration, InMemoryBucket, Limiter, Rate
from pytest_httpx import HTTPXMock

from simyan.cache import SQLiteCache
from simyan.comicvine import Comicvine
from simyan.errors import RateLimitError

SLEEP_TARGET: Final[str] = "pyrate_limiter.limiter.sleep"
TEST_ENDPOINT: Final[str] = "/rate-limited/"
TEST_URL: Final[str] = f"https://comicvine.gamespot.com/api{TEST_ENDPOINT}"
SUCCESS_JSON: Final[dict] = {"results": []}
FAILURE_JSON: Final[dict] = {"error": "Rate Limited"}
REQUEST_DURATION: Final[float] = 0.1
MIN_SECOND: Final[float] = 1 * 0.85
MAX_SECOND: Final[float] = 1 * 1.15
MIN_HOUR: Final[float] = 3_600 * 0.85
MAX_HOUR: Final[float] = 3_600 * 1.15


def add_200_response(mock: HTTPXMock) -> None:
    mock.add_response(status_code=200, json=SUCCESS_JSON, is_reusable=True)


def add_429_response(mock: HTTPXMock) -> None:
    mock.add_response(status_code=429, json=FAILURE_JSON, is_reusable=True)


def make_limiter(*rates: Rate) -> Limiter:
    return Limiter(InMemoryBucket(list(rates)))


def make_session(limiter: Limiter) -> Comicvine:
    return Comicvine(
        api_key="UNSET", cache=SQLiteCache(path=Path("tests/cache.sqlite")), limiter=limiter
    )


@pytest.fixture
def second_session() -> Comicvine:
    return make_session(limiter=make_limiter(Rate(2, Duration.SECOND)))


@pytest.fixture
def hour_session() -> Comicvine:
    return make_session(limiter=make_limiter(Rate(5, Duration.HOUR)))


@pytest.fixture
def dual_session() -> Comicvine:
    return make_session(limiter=make_limiter(Rate(2, Duration.SECOND), Rate(5, Duration.HOUR)))


class TestSecondLimit:
    def test_within_limit_not_delayed(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, second_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)

        with patch(SLEEP_TARGET) as mock_sleep:
            for _ in range(2):
                second_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

        mock_sleep.assert_not_called()

    def test_exceeding_limit_causes_sleep(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, second_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)

        with patch(SLEEP_TARGET) as mock_sleep:
            for _ in range(3):
                second_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

        mock_sleep.assert_called_once()
        sleep_duration = mock_sleep.call_args[0][0]
        assert MIN_SECOND <= sleep_duration <= MAX_SECOND

    def test_two_full_requests_require_one_sleep(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, second_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)
        sleep_calls: list[float] = []

        def _fake_sleep(duration: float) -> None:
            sleep_calls.append(duration)
            freezer.tick(duration)

        with patch(SLEEP_TARGET, side_effect=_fake_sleep):
            for _ in range(4):
                second_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

        assert len(sleep_calls) == 1
        assert MIN_SECOND <= sleep_calls[0] <= MAX_SECOND

    def test_refills_after_sleep(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, second_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)

        for _ in range(2):
            second_session._perform_get_request(endpoint=TEST_ENDPOINT)
            freezer.tick(REQUEST_DURATION)
        freezer.move_to(timedelta(seconds=1))
        with patch(SLEEP_TARGET) as mock_sleep:
            for _ in range(2):
                second_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

        mock_sleep.assert_not_called()


class TestHourLimit:
    def test_within_limit_not_delayed(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, hour_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)

        with patch(SLEEP_TARGET) as mock_sleep:
            for _ in range(5):
                hour_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

        mock_sleep.assert_not_called()

    def test_exceeding_limit_sleep(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, hour_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)

        with patch(SLEEP_TARGET) as mock_sleep:
            for _ in range(6):
                hour_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

        mock_sleep.assert_called_once()
        sleep_duration = mock_sleep.call_args[0][0]
        assert MIN_HOUR <= sleep_duration <= MAX_HOUR

    def test_refills_after_sleep(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, hour_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)

        for _ in range(5):
            hour_session._perform_get_request(endpoint=TEST_ENDPOINT)
            freezer.tick(REQUEST_DURATION)
        freezer.move_to(timedelta(hours=1))
        with patch(SLEEP_TARGET) as mock_sleep:
            for _ in range(5):
                hour_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

        mock_sleep.assert_not_called()


class TestDualLimit:
    def test_fails_second_passes_hour(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, dual_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)
        sleep_calls: list[float] = []

        def _fake_sleep(duration: float) -> None:
            sleep_calls.append(duration)
            freezer.tick(duration)

        with patch(SLEEP_TARGET, side_effect=_fake_sleep):
            for _ in range(3):
                dual_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

        long_sleeps = [s for s in sleep_calls if MIN_HOUR <= s <= MAX_HOUR]
        short_sleeps = [s for s in sleep_calls if MIN_SECOND <= s <= MAX_SECOND]

        assert len(long_sleeps) == 0
        assert len(short_sleeps) == 1

    def test_passes_second_fails_hour(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, dual_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)
        sleep_calls: list[float] = []

        def _fake_sleep(duration: float) -> None:
            sleep_calls.append(duration)
            freezer.tick(duration)

        with patch(SLEEP_TARGET, side_effect=_fake_sleep):
            for _ in range(5):
                dual_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)
                freezer.move_to(timedelta(seconds=1))
            freezer.move_to(timedelta(minutes=1))
            dual_session._perform_get_request(endpoint=TEST_ENDPOINT)

        long_sleeps = [s for s in sleep_calls if MIN_HOUR <= s <= MAX_HOUR]
        short_sleeps = [s for s in sleep_calls if MIN_SECOND <= s <= MAX_SECOND]

        assert len(short_sleeps) == 0
        assert len(long_sleeps) == 1

    def test_both_buckets_are_enforced(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, dual_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)
        sleep_calls: list[float] = []

        def _fake_sleep(duration: float) -> None:
            sleep_calls.append(duration)
            freezer.tick(duration)

        with patch(SLEEP_TARGET, side_effect=_fake_sleep):
            for _ in range(4):
                dual_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

            long_sleeps = [s for s in sleep_calls if MIN_HOUR <= s <= MAX_HOUR]
            short_sleeps = [s for s in sleep_calls if MIN_SECOND <= s <= MAX_SECOND]
            assert len(long_sleeps) == 0
            assert len(short_sleeps) == 1

            for _ in range(2):
                dual_session._perform_get_request(endpoint=TEST_ENDPOINT)

            long_sleeps = [s for s in sleep_calls if MIN_HOUR <= s <= MAX_HOUR]
            short_sleeps = [s for s in sleep_calls if MIN_SECOND <= s <= MAX_SECOND]
            assert len(long_sleeps) == 1
            assert len(short_sleeps) == 2

    def test_no_sleep_within_both_limits(
        self, freezer: FrozenDateTimeFactory, httpx_mock: HTTPXMock, dual_session: Comicvine
    ) -> None:
        add_200_response(mock=httpx_mock)

        with patch(SLEEP_TARGET) as mock_sleep:
            for _ in range(2):
                dual_session._perform_get_request(endpoint=TEST_ENDPOINT)
                freezer.tick(REQUEST_DURATION)

        mock_sleep.assert_not_called()


class TestRateLimitError:
    def test_server_429_raises_rate_limit_error(
        self, httpx_mock: HTTPXMock, second_session: Comicvine
    ) -> None:
        add_429_response(mock=httpx_mock)

        with pytest.raises(RateLimitError):
            second_session._perform_get_request(endpoint=TEST_ENDPOINT)

    def test_server_429_raised_after_ratelimiting(
        self, httpx_mock: HTTPXMock, second_session: Comicvine
    ) -> None:
        httpx_mock.add_response(status_code=200, json=SUCCESS_JSON)
        httpx_mock.add_response(status_code=200, json=SUCCESS_JSON)
        httpx_mock.add_response(status_code=429, json=FAILURE_JSON)

        with patch(SLEEP_TARGET) as mock_sleep:
            for _ in range(2):
                second_session._perform_get_request(endpoint=TEST_ENDPOINT)
            with pytest.raises(RateLimitError):
                second_session._perform_get_request(endpoint=TEST_ENDPOINT)

        mock_sleep.assert_called_once()
