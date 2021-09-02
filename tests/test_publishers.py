import pytest

from Simyan.exceptions import APIError

ID = 10
LOCATION_ADDRESS = "4000 Warner Blvd"
LOCATION_CITY = "Burbank"
LOCATION_STATE = "California"
NAME = "DC Comics"
STORY_ARC_ID = 40503
STORY_ARC_NAME = "The Killing Joke"
VOLUME_ID = 771
VOLUME_NAME = "Movie Comics"


def test_publisher(talker):
    result = talker.publisher(ID)
    assert result.id == ID
    assert result.location_address == LOCATION_ADDRESS
    assert result.location_city == LOCATION_CITY
    assert result.location_state == LOCATION_STATE
    assert result.name == NAME
    assert result.story_arcs[0].id == STORY_ARC_ID
    assert result.story_arcs[0].name == STORY_ARC_NAME
    assert result.volumes[0].id == VOLUME_ID
    assert result.volumes[0].name == VOLUME_NAME


def test_publisher_fail(talker):
    with pytest.raises(APIError):
        talker.publisher(-1)


def test_publisher_list(talker):
    search_results = talker.publisher_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.id == ID
    assert result.location_address == LOCATION_ADDRESS
    assert result.location_city == LOCATION_CITY
    assert result.location_state == LOCATION_STATE
    assert result.name == NAME


def test_publisher_list_empty(talker):
    results = talker.publisher_list({"filter": "name:INVALID"})
    assert len(results) == 0
