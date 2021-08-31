import pytest

from Simyan.exceptions import APIError

PUBLISHER_ID = 10
PUBLISHER_NAME = "DC Comics"


def test_publisher(talker):
    result = talker.publisher(PUBLISHER_ID)
    assert result.id == PUBLISHER_ID
    assert result.name == PUBLISHER_NAME


def test_publisher_fail(talker):
    with pytest.raises(APIError):
        talker.publisher(-1)


def test_publisher_list(talker):
    search_results = talker.publisher_list({"filter": f"name:{PUBLISHER_NAME}"})
    result = [x for x in search_results if x.id == PUBLISHER_ID][0]
    assert result.id == PUBLISHER_ID
    assert result.name == PUBLISHER_NAME


def test_publisher_list_empty(talker):
    results = talker.publisher_list({"filter": "name:INVALID"})
    assert len(results) == 0
