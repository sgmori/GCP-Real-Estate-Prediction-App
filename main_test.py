import concurrent.futures
from unittest import mock

from google.cloud import bigquery
import pytest


@pytest.fixture
def flask_client():
    import main

    main.app.testing = True
    return main.app.test_client()


def test_main(flask_client):
    r = flask_client.get("/")
    assert r.status_code == 302
    assert "/results" in r.headers.get("location", "")


def test_results(flask_client, monkeypatch):
    import main

    fake_job = mock.create_autospec(bigquery.QueryJob)
    fake_rows = [("example1.com", "42"), ("example2.com", "38")]
    fake_job.result.return_value = fake_rows

    def fake_get_job(self, job_id, **kwargs):
        return fake_job

    monkeypatch.setattr(main.bigquery.Client, "get_job", fake_get_job)

    r = flask_client.get(
        "/results?project_id=123&job_id=456&location=my_location"
    )
    response_body = r.data.decode("utf-8")

    assert r.status_code == 200
    assert "Query Result" in response_body  # verifies header
    assert "example2.com" in response_body
    assert "42" in response_body
