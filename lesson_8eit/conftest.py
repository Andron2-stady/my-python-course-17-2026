import uuid
import pytest
from yougile_api import YougileClient


@pytest.fixture(scope="session")
def client():
    return YougileClient()


@pytest.fixture(scope="function")
def project_data():
    unique_name = f"test-project-{uuid.uuid4().hex[:8]}"
    return {
        "title": unique_name,
        "description": "Project for automated tests"
    }


@pytest.fixture(scope="function")
def created_project(client, project_data):
    """Создаёт проект и удаляет его после теста."""
    response = client.create_project(project_data)
    assert response.status_code == 201
    project_id = response.json()["id"]

    yield project_id

    # Очистка: удаляем проект даже при падении теста
    try:
        client.delete_project(project_id)
    except Exception:
        pass
