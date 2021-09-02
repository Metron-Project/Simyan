import pytest

from Simyan.exceptions import APIError

CREATOR_ID = 40439
CREATOR_NAME = "Geoff Johns"
CREATOR_COUNT = "67"
FIRST_ISSUE_ID = 111265
FIRST_ISSUE_NAME = "Airborne"
FIRST_ISSUE_NUMBER = "1"
ID = 18216
ISSUE_COUNT = 67
ISSUE_ID = 106713
ISSUE_NAME = "Wanted: Hal Jordan Part 4"
ISSUE_NUMBER = "17"
LAST_ISSUE_ID = 278617
LAST_ISSUE_NAME = "War of the Green Lanterns, Part Ten"
LAST_ISSUE_NUMBER = "67"
NAME = "Green Lantern"
PUBLISHER_ID = 10
PUBLISHER_NAME = "DC Comics"
START_YEAR = "2005"


def test_volume(talker):
    result = talker.volume(ID)
    assert result.creators[0].id == CREATOR_ID
    assert result.creators[0].name == CREATOR_NAME
    assert result.creators[0].count == CREATOR_COUNT
    assert result.first_issue.id == FIRST_ISSUE_ID
    assert result.first_issue.name == FIRST_ISSUE_NAME
    assert result.first_issue.number == FIRST_ISSUE_NUMBER
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.issues[0].id == ISSUE_ID
    assert result.issues[0].name == ISSUE_NAME
    assert result.issues[0].number == ISSUE_NUMBER
    assert result.last_issue.id == LAST_ISSUE_ID
    assert result.last_issue.name == LAST_ISSUE_NAME
    assert result.last_issue.number == LAST_ISSUE_NUMBER
    assert result.name == NAME
    assert result.publisher.id == PUBLISHER_ID
    assert result.publisher.name == PUBLISHER_NAME
    assert result.start_year == START_YEAR


def test_volume_fail(talker):
    with pytest.raises(APIError):
        talker.volume(-1)


def test_volume_list(talker):
    search_results = talker.volume_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.first_issue.id == FIRST_ISSUE_ID
    assert result.first_issue.name == FIRST_ISSUE_NAME
    assert result.first_issue.number == FIRST_ISSUE_NUMBER
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert result.last_issue.id == LAST_ISSUE_ID
    assert result.last_issue.name == LAST_ISSUE_NAME
    assert result.last_issue.number == LAST_ISSUE_NUMBER
    assert result.name == NAME
    assert result.publisher.id == PUBLISHER_ID
    assert result.publisher.name == PUBLISHER_NAME
    assert result.start_year == START_YEAR


def test_volume_list_empty(talker):
    results = talker.volume_list({"filter": "name:INVALID"})
    assert len(results) == 0
