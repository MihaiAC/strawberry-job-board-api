import pytest
from app.db.data import EMPLOYERS_DATA, JOBS_DATA


@pytest.mark.api
@pytest.mark.mutation
def test_add_employer_complete_info(test_client, graphql_endpoint):
    employer_name = "X name"
    employer_industry = "YZ industry"
    employer_email = "XYZ@example.com"
    query = f"""
    mutation {{
        addEmployer(name: "{employer_name}", industry: "{employer_industry}" contactEmail: "{employer_email}") {{
            id
            name
            industry
            contactEmail
            jobs {{
                id
            }}
        }}
    }}
    """
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
    employer = result["data"]["addEmployer"]
    assert employer["id"] == len(EMPLOYERS_DATA) + 1
    assert employer["name"] == employer_name
    assert employer["industry"] == employer_industry
    assert employer["contactEmail"] == employer_email

    assert len(employer["jobs"]) == 0
