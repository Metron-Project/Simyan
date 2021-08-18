PUBLISHER_ID = 10
VOLUME_ID = 18216
VOLUME_NAME = 'Green Lantern'
VOLUME_START_YEAR = '2005'


def test_volume(talker):
    result = talker.volume(VOLUME_ID)
    assert result.publisher.id == PUBLISHER_ID
    assert result.id == VOLUME_ID
    assert result.name == VOLUME_NAME
    assert result.start_year == VOLUME_START_YEAR


def test_volume_list(talker):
    result = talker.volume_list({'filter': f"publisher:{PUBLISHER_ID},name:{VOLUME_NAME}"})
    assert len([x for x in result if x.publisher.id == PUBLISHER_ID and x.id == VOLUME_ID and x.name == VOLUME_NAME and x.start_year == VOLUME_START_YEAR]) == 1
