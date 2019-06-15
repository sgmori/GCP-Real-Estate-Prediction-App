import pytest


@pytest.fixture
def flaskclient():
    import main

    main.app.testing = True
    return main.app.test_client()


def test_main(flask_client):
    r = flask_client.get("/")
    assert r.status_code == 302
    assert "/results" in r.headers.get("location", "")
