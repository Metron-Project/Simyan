import pytest

from Simyan.exceptions import APIError

PUBLISHER_ID = 10
VOLUME_ID = 18216
VOLUME_NAME = "Green Lantern"
VOLUME_START_YEAR = "2005"


def test_volume(talker):
    result = talker.volume(VOLUME_ID)
    assert result.id == VOLUME_ID
    assert result.publisher.id == PUBLISHER_ID
    assert result.name == VOLUME_NAME
    assert result.start_year == VOLUME_START_YEAR


def test_volume_fail(talker):
    with pytest.raises(APIError):
        talker.volume(-1)


def test_volume_list(talker):
    search_results = talker.volume_list({"filter": f"name:{VOLUME_NAME}"})
    result = [x for x in search_results if x.id == VOLUME_ID][0]
    assert result.publisher.id == PUBLISHER_ID
    assert result.id == VOLUME_ID
    assert result.name == VOLUME_NAME
    assert result.start_year == VOLUME_START_YEAR


def test_volume_list_empty(talker):
    results = talker.volume_list({"filter": "name:INVALID"})
    assert len(results) == 0
