import requests
import os
from django.conf import settings

class NotionService:
    def __init__(self):
        self.api_key = settings.NOTION_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.base_url = "https://api.notion.com/v1"

    def query_database(self, db_id, filter_data=None):
        url = f"{self.base_url}/databases/{db_id}/query"
        payload = {}
        if filter_data:
            payload['filter'] = filter_data
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json().get("results", [])

    def create_page(self, db_id, properties):
        url = f"{self.base_url}/pages"
        payload = {"parent": {"database_id": db_id}, "properties": properties}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def update_page(self, page_id, properties):
        url = f"{self.base_url}/pages/{page_id}"
        payload = {"properties": properties}
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
        
    def delete_page(self, page_id):
        url = f"{self.base_url}/pages/{page_id}"
        payload = {"archived": True}
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()