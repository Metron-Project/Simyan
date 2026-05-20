import pytest
from responses import RequestsMock as Mocker
from responses.matchers import query_param_matcher

from simyan.comicvine import Comicvine, ComicvineResource
from simyan.errors import ServiceError
from simyan.schemas.origin import BasicOrigin


def test_get_origin(session: Comicvine) -> None:
    result = session.get_origin(origin_id=1)
    assert result is not None
    assert result.id == 1

    assert result.character_set is None
    assert len(result.characters) == 4548
    assert len(result.profiles) == 0


def test_get_origin_fail(
    mock_session: Comicvine, mock_params: dict[str, str], mock_params_str: str
) -> None:
    with Mocker(assert_all_requests_are_fired=True) as mock:
        url = (
            f"https://comicvine.gamespot.mock/api/origin/{ComicvineResource.ORIGIN.resource_id}--1/"
        )
        mock.get(
            url=url,
            match=[query_param_matcher(mock_params)],
            status=404,
            json={"detail": "Not found."},
        )
        with pytest.raises(ServiceError):
            mock_session.get_origin(origin_id=-1)
        mock.assert_call_count(f"{url}?{mock_params_str}", 1)


def test_list_origins(session: Comicvine) -> None:
    search_results = session.list_origins({"filter": "name:Mutant"})
    assert len(search_results) != 0
    result = next(x for x in search_results if x.id == 1)
    assert result is not None

    assert str(result.api_url) == "https://comicvine.gamespot.com/api/origin/4030-1/"
    assert result.name == "Mutant"
    assert str(result.site_url) == "https://comicvine.gamespot.com/mutant/4030-1/"


def test_list_origins_empty(session: Comicvine) -> None:
    results = session.list_origins({"filter": "name:Invalid Origin Name"})
    assert len(results) == 0


def test_list_origins_max_results(session: Comicvine) -> None:
    results = session.list_origins(max_results=3)
    assert len(results) == 3


def test_search_origin(session: Comicvine) -> None:
    results = session.search(resource=ComicvineResource.ORIGIN, query="Mutant")
    assert all(isinstance(x, BasicOrigin) for x in results)
