from starlette.testclient import TestClient


def post_graphql(
    test_client: TestClient,
    graphql_endpoint: str,
    query: str,
    expected_status: int = 200,
) -> dict:
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == expected_status
    return response.json()
