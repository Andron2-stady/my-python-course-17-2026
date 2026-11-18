import pytest


class TestYouGileProjectsAPI:
    def test_create_project_positive(self, client, project_data):
        response = client.create_project(project_data)

        assert response.status_code == 201
        assert "id" in response.json()

        # Проверяем название через GET, так как в ответе POST только id
        project_id = response.json()["id"]
        get_resp = client.get_project(project_id)
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == project_data["title"]

    def test_create_project_negative_empty_title(self, client):
        response = client.create_project({"title": ""})

        assert response.status_code == 400
        # Проверяем, что сервер ругается именно на поле title
        assert "title" in response.text.lower()

    def test_update_project_positive(self, created_project, client):
        project_id = created_project
        new_title = "Updated title"

        response = client.update_project(project_id, {"title": new_title})
        assert response.status_code == 200

        get_resp = client.get_project(project_id)
        assert get_resp.json()["title"] == new_title

    def test_update_project_negative_not_found(self, client):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.update_project(fake_id, {"title": "Test"})

        assert response.status_code == 404
        assert "not found" in response.text.lower()

    def test_get_project_positive(self, created_project, client):
        project_id = created_project
        response = client.get_project(project_id)

        assert response.status_code == 200
        assert response.json()["id"] == project_id
        assert "title" in response.json()

    def test_get_project_negative_not_found(self, client):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get_project(fake_id)

        assert response.status_code == 404
        assert "not found" in response.text.lower()
