from .base_service import NotionService
from django.conf import settings

class AdminService(NotionService):
    def __init__(self):
        super().__init__()
        self.db_id = settings.NOTION_MAINADMIN_DB_ID

    def find_admin_by_email(self, email):
        filter_data = {"property": "email", "email": {"equals": email}}
        results = self.query_database(self.db_id, filter_data)
        return results[0] if results else None