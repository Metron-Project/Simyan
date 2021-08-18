PUBLISHER_ID = 10
PUBLISHER_NAME = 'DC Comics'


def test_publisher(talker):
    result = talker.publisher(PUBLISHER_ID)
    assert result.name == PUBLISHER_NAME


def test_publisher_list(talker):
    result = talker.publisher_list({'filter': f"name:{PUBLISHER_NAME}"})
    assert len([x for x in result if x.id == PUBLISHER_ID and x.name == PUBLISHER_NAME]) == 1
