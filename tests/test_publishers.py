import pytest

from Simyan import APIError

PUBLISHER_ID = 10
PUBLISHER_NAME = 'DC Comics'


def test_publisher(talker):
    result = talker.publisher(PUBLISHER_ID)
    assert result.name == PUBLISHER_NAME


def test_publisher_fail(talker):
    with pytest.raises(APIError):
        talker.publisher(-1)


def test_publisher_list(talker):
    results = talker.publisher_list({'filter': f"name:{PUBLISHER_NAME}"})
    assert len([x for x in results if x.id == PUBLISHER_ID and x.name == PUBLISHER_NAME]) == 1


def test_publisher_list_empty(talker):
    results = talker.publisher_list({'filter': 'name:INVALID'})
    assert len(results) == 0
