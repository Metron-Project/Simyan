import pytest

from Simyan.exceptions import APIError

COUNTRY = "United States"
DATE_OF_BIRTH = None
DATE_OF_DEATH = None
EMAIL = None
GENDER = 1
HOMETOWN = None
ID = 41853
ISSUE_COUNT = None
ISSUES_COUNT = 1386
ISSUE_ID = 878411
ISSUE_NAME = None
NAME = "Peter J. Tomasi"
STORY_ARCS_COUNT = 5
STORY_ARC_ID = 60628
STORY_ARC_NAME = "Destiny"
VOLUMES_COUNT = 374
VOLUME_ID = 4958
VOLUME_NAME = "DC Universe: Trinity"
WEBSITE = None


def test_creator(talker):
    result = talker.creator(ID)
    assert result.country == COUNTRY
    assert result.date_of_birth == DATE_OF_BIRTH
    assert result.date_of_death == DATE_OF_DEATH
    assert result.email == EMAIL
    assert result.gender == GENDER
    assert result.hometown == HOMETOWN
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    assert len(result.issues) == ISSUES_COUNT
    assert result.issues[0].id == ISSUE_ID
    assert result.issues[0].name == ISSUE_NAME
    assert result.name == NAME
    assert len(result.story_arcs) == STORY_ARCS_COUNT
    assert result.story_arcs[0].id == STORY_ARC_ID
    assert result.story_arcs[0].name == STORY_ARC_NAME
    assert len(result.volumes) == VOLUMES_COUNT
    assert result.volumes[0].id == VOLUME_ID
    assert result.volumes[0].name == VOLUME_NAME
    assert result.website == WEBSITE


def test_creator_fail(talker):
    with pytest.raises(APIError):
        talker.creator(-1)


def test_creator_list(talker):
    search_results = talker.creator_list({"filter": f"name:{NAME}"})
    result = [x for x in search_results if x.id == ID][0]
    assert result.country == COUNTRY
    assert result.date_of_birth == DATE_OF_BIRTH
    assert result.date_of_death == DATE_OF_DEATH
    assert result.email == EMAIL
    assert result.gender == GENDER
    assert result.hometown == HOMETOWN
    assert result.id == ID
    assert result.issue_count == ISSUE_COUNT
    # Search doesn't contain Issues
    assert result.name == NAME
    # Search doesn't contain Story Arcs
    # Search doesn't contain Volumes
    assert result.website == WEBSITE


def test_creator_list_empty(talker):
    results = talker.creator_list({"filter": "name:INVALID"})
    assert len(results) == 0
