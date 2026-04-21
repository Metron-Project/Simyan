from datetime import datetime

import pytest

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.power import BasicPower


def test_get_power(session: Comicvine) -> None:
    result = session.get_power(power_id=1)
    assert result is not None
    assert result.id == 1

    assert len(result.characters) == 8425


def test_get_power_fail(session: Comicvine) -> None:
    with pytest.raises(ServiceError):
        session.get_power(power_id=-1)


def test_list_powers(session: Comicvine) -> None:
    search_results = session.list_powers({"filter": "name:Flight"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 1)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/power/4035-1/"
    assert result.date_added == datetime(2008, 6, 6, 11, 28, 15)
    assert result.name == "Flight"
    assert (
        str(result.site_url)
        == "https://comicvine.gamespot.com/characters/?wikiSlug=flight&wikiTypeId=4035&wikiId=1&powers%5B%5D=1"
    )


def test_list_powers_empty(session: Comicvine) -> None:
    results = session.list_powers({"filter": "name:Invalid Power Name"})
    assert len(results) == 0


def test_list_powers_max_results(session: Comicvine) -> None:
    results = session.list_powers(max_results=10)
    assert len(results) == 10


def test_search_power(session: Comicvine) -> None:
    results = session.search(resource=ComicvineResource.POWER, query="Flight")
    assert all(isinstance(x, BasicPower) for x in results)
