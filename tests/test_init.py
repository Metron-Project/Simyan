import pytest

from Simyan import api, Session, AuthenticationError


def test_api():
    with pytest.raises(AuthenticationError):
        api()

    m = None
    try:
        m = api(api_key="Something")
    except Exception as exc:
        print(f"Simyan.api() raised {exc} unexpectedly!")

    assert m.__class__.__name__ == Session.__name__
