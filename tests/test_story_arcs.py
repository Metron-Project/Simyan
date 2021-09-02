import pytest

from Simyan.exceptions import APIError

FIRST_ISSUE_ID = 155207
FIRST_ISSUE_NAME = "Agent Orange Part 1"
FIRST_ISSUE_NUMBER = "39"
ID = 55766
ISSUE_COUNT = 0
ISSUE_ID = 155207
ISSUE_NAME = "Agent Orange Part 1"
NAME = "Blackest Night"
PUBLISHER_ID = 10
PUBLISHER_NAME = "DC Comics"


def test_story_arc(talker):
    result = talker.story_arc(ID)
    assert result.first_issue.id == FIRST_ISSUE_ID
    assert result.first_issue.name == FIRST_ISSUE_NAME
    assert result.first_issue.number == FIRST_ISSUE_NUMBER
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.issues[0].id == ISSUE_ID
    assert result.issues[0].name == ISSUE_NAME
    assert result.name == NAME
    assert result.publisher.id == PUBLISHER_ID
    assert result.publisher.name == PUBLISHER_NAME


def test_story_arc_fail(talker):
    with pytest.raises(APIError):
        talker.story_arc(-1)


def test_story_arc_list(talker):
    search_results = talker.story_arc_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.first_issue.id == FIRST_ISSUE_ID
    assert result.first_issue.name == FIRST_ISSUE_NAME
    assert result.first_issue.number == FIRST_ISSUE_NUMBER
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.name == NAME
    assert result.publisher.id == PUBLISHER_ID
    assert result.publisher.name == PUBLISHER_NAME


def test_story_arc_list_empty(talker):
    results = talker.story_arc_list({"filter": "name:INVALID"})
    assert len(results) == 0
