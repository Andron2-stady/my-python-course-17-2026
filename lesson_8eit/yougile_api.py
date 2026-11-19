import os
import requests
from dotenv import load_dotenv


class YougileClient:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("YOUGILE_BASE_URL")
        self.api_key = os.getenv("YOUGILE_API_KEY")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def create_project(self, data: dict):
        """Создаёт новый проект."""
        return self.session.post(f"{self.base_url}/api-v2/projects", json=data)

    def update_project(self, project_id: str, data: dict):
        """Обновляет проект."""
        return self.session.put(f"{self.base_url}/api-v2/projects/{
            project_id}", json=data)

    def get_project(self, project_id: str):
        """Получает информацию о проекте."""
        return self.session.get(f"{self.base_url}/api-v2/projects/{
            project_id}")

    def delete_project(self, project_id: str):
        """Удаляет проект (мягкое удаление)."""
        return self.session.put(
            f"{self.base_url}/api-v2/projects/{project_id}",
            json={"deleted": True}
        )
