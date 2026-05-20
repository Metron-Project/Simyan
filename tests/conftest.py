import os
from datetime import timedelta
from pathlib import Path

import pytest
from requests_cache import NEVER_EXPIRE

from simyan.comicvine import Comicvine


@pytest.fixture(scope="session")
def api_key() -> str:
    return os.getenv("COMICVINE__API_KEY", default="UNSET")


@pytest.fixture
def session(api_key: str, tmp_path: Path) -> Comicvine:
    return Comicvine(
        api_key=api_key,
        cache_path=Path("tests") / "cache.sqlite",
        cache_expiry=NEVER_EXPIRE,
        ratelimit_path=tmp_path / "simyan-ratelimit.sqlite",
    )


@pytest.fixture
def mock_session(tmp_path: Path) -> Comicvine:
    return Comicvine(
        api_key="UNSET",
        base_url="https://comicvine.gamespot.mock/api",
        cache_path=tmp_path / "simyan.sqlite",
        cache_expiry=timedelta(seconds=1),
        ratelimit_path=tmp_path / "simyan-ratelimit.sqlite",
    )


@pytest.fixture
def mock_params() -> dict[str, str]:
    return {"api_key": "UNSET", "format": "json"}


@pytest.fixture
def mock_params_str(mock_params: dict[str, str]) -> str:
    return "&".join(f"{k}={v}" for k, v in mock_params.items())
