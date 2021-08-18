VOLUME_ID = 18216
ISSUE_ID = 111265
ISSUE_NUMBER = '1'


def test_issue(talker):
    result = talker.issue(ISSUE_ID)
    assert result.volume.id == VOLUME_ID
    assert result.id == ISSUE_ID
    assert result.issue_number == ISSUE_NUMBER


def test_issue_list(talker):
    result = talker.issue_list({'filter': f"volume:{VOLUME_ID},issue_number:{ISSUE_NUMBER}"})
    assert len([x for x in result if x.volume.id == VOLUME_ID and x.id == ISSUE_ID and x.issue_number == ISSUE_NUMBER]) == 1
