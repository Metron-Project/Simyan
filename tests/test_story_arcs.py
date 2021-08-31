import pytest

from Simyan.exceptions import APIError

PUBLISHER_ID = 10
STORY_ARC_ID = 55766
STORY_ARC_NAME = "Blackest Night"


def test_story_arc(talker):
    result = talker.story_arc(STORY_ARC_ID)
    assert result.id == STORY_ARC_ID
    assert result.publisher.id == PUBLISHER_ID
    assert result.name == STORY_ARC_NAME


def test_story_arc_fail(talker):
    with pytest.raises(APIError):
        talker.story_arc(-1)


def test_story_arc_list(talker):
    search_results = talker.story_arc_list({"filter": f"name:{STORY_ARC_NAME}"})
    result = [x for x in search_results if x.id == STORY_ARC_ID][0]
    assert result.id == STORY_ARC_ID
    assert result.publisher.id == PUBLISHER_ID
    assert result.name == STORY_ARC_NAME


def test_story_arc_list_empty(talker):
    results = talker.story_arc_list({"filter": "name:INVALID"})
    assert len(results) == 0
