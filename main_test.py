import concurrent.futures
from unittest import mock

from google.cloud import bigquery
import pytest


@pytest.fixture
def flaskclient():
    import main

    main.app.testing = True
    return main.app.test_client()


def test_main(flaskclient):
    r = flaskclient.get("/")
    assert r.status_code == 302
    assert "/results" in r.headers.get("location", "")
