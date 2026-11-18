import uuid
import pytest
from yougile_client import YouGileClient


@pytest.fixture(scope="session")
def client():
    return YouGileClient()


@pytest.fixture(scope="function")
def project_data():
    unique_name = f"test-project-{uuid.uuid4().hex[:8]}"
    return {
        "title": unique_name,
        "description": "Project for automated tests"
    }


@pytest.fixture(scope="function")
def created_project(client, project_data):

    # Создаем проект
    response = client.create_project(project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    # Передаем ID теста
    yield project_id

    # Очистка (выполнится всегда, даже при падении теста)
    try:
        client.delete_project(project_id)
    except Exception:
        pass
