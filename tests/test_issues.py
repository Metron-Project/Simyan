from datetime import date

import pytest

from Simyan.exceptions import APIError

COVER_DATE = date(year=2005, month=7, day=1)
FIRST_APPEARANCE_STORY_ARCS = None
ID = 111265
NAME = "Airborne"
NUMBER = "1"
CREATOR_ID = 10945
CREATOR_NAME = "Alex Ross"
CREATOR_ROLES = "inker, colorist, cover"
STORE_DATE = date(year=2005, month=5, day=18)
STORY_ARC_ID = 54588
STORY_ARC_NAME = "Green Lantern: Rebirth"
VOLUME_ID = 18216
VOLUME_NAME = "Green Lantern"


def test_issue(talker):
    result = talker.issue(ID)
    assert result.cover_date == COVER_DATE
    assert result.first_appearance_story_arcs == FIRST_APPEARANCE_STORY_ARCS
    assert result.id == ID
    assert result.name == NAME
    assert result.number == NUMBER
    assert result.creators[0].id == CREATOR_ID
    assert result.creators[0].name == CREATOR_NAME
    assert result.creators[0].roles == CREATOR_ROLES
    assert result.store_date == STORE_DATE
    assert result.story_arcs[0].id == STORY_ARC_ID
    assert result.story_arcs[0].name == STORY_ARC_NAME
    assert result.volume.id == VOLUME_ID
    assert result.volume.name == VOLUME_NAME


def test_issue_fail(talker):
    with pytest.raises(APIError):
        talker.issue(-1)


def test_issue_list(talker):
    search_results = talker.issue_list({"filter": f"volume:{VOLUME_ID},issue_number:{NUMBER}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.cover_date == COVER_DATE
    assert result.id == ID
    assert result.name == NAME
    assert result.number == NUMBER
    assert result.store_date == STORE_DATE
    assert result.volume.id == VOLUME_ID
    assert result.volume.name == VOLUME_NAME


def test_issue_list_empty(talker):
    results = talker.issue_list({"filter": "name:INVALID"})
    assert len(results) == 0


def test_issue_bad_cover_date(talker):
    xmen_2 = talker.issue(6787)
    assert xmen_2.store_date is None
    assert xmen_2.cover_date == date(1963, 11, 1)
    assert xmen_2.id == 6787
    assert xmen_2.number == "2"
    assert len(xmen_2.creators) == 4
    assert xmen_2.creators[0].name == "Jack Kirby"
    assert xmen_2.creators[0].roles == "penciler"
    assert len(xmen_2.characters) == 10
    assert xmen_2.characters[0].name == "Angel"
