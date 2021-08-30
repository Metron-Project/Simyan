import datetime

import pytest

from Simyan.exceptions import APIError

VOLUME_ID = 18216
ISSUE_ID = 111265
ISSUE_NUMBER = '1'


def test_issue(talker):
    result = talker.issue(ISSUE_ID)
    assert result.volume.id == VOLUME_ID
    assert result.id == ISSUE_ID
    assert result.issue_number == ISSUE_NUMBER


def test_issue_fail(talker):
    with pytest.raises(APIError):
        talker.issue(-1)


def test_issue_list(talker):
    results = talker.issue_list({'filter': f"volume:{VOLUME_ID},issue_number:{ISSUE_NUMBER}"})
    assert len([x for x in results if x.volume.id == VOLUME_ID and x.id == ISSUE_ID and x.issue_number == ISSUE_NUMBER]) == 1


def test_issue_list_empty(talker):
    results = talker.issue_list({'filter': 'name:INVALID'})
    assert len(results) == 0


def test_issue_bad_cover_date(talker):
    xmen_2 = talker.issue(6787)
    assert xmen_2.store_date is None
    assert xmen_2.cover_date == datetime.date(1963, 11, 1)
    assert xmen_2.id == 6787
    assert xmen_2.issue_number == "2"
    assert len(xmen_2.person_credits) == 4
    assert xmen_2.person_credits[0].name == "Jack Kirby"
    assert xmen_2.person_credits[0].role == "penciler"
    assert len(xmen_2.character_credits) == 10
    assert xmen_2.character_credits[0].name == "Angel"
