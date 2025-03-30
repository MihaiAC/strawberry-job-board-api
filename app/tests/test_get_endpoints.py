import pytest
from app.db.data import JOBS_DATA, EMPLOYERS_DATA


@pytest.mark.api
@pytest.mark.sql
def test_get_jobs(test_client, jobs_endpoint):
    response = test_client.get(jobs_endpoint)
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json) == len(JOBS_DATA)
    for idx, job_json in enumerate(response_json):
        assert job_json["title"] == JOBS_DATA[idx]["title"]


@pytest.mark.api
@pytest.mark.sql
def test_get_employers(test_client, employers_endpoint):
    response = test_client.get(employers_endpoint)
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json) == len(EMPLOYERS_DATA)
    for idx, employer_json in enumerate(response_json):
        assert employer_json["name"] == EMPLOYERS_DATA[idx]["name"]
