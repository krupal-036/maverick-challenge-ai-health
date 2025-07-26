from .base_service import NotionService
from django.conf import settings
import uuid
import bcrypt
from datetime import datetime

class PatientService(NotionService):
    def __init__(self):
        super().__init__()
        self.db_id = settings.NOTION_PATIENT_DB_ID

    def find_patient_by_email(self, email):
        filter_data = {"property": "email", "email": {"equals": email}}
        results = self.query_database(self.db_id, filter_data)
        return results[0] if results else None

    def create_patient(self, data):
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        properties = {
            "id": {"title": [{"text": {"content": str(uuid.uuid4())}}]},
            "full_name": {"rich_text": [{"text": {"content": data['full_name']}}]},
            "email": {"email": data['email']},
            "password_hash": {"rich_text": [{"text": {"content": hashed_password}}]},
            "phone_number": {"phone_number": data['phone_number']},
            "gender": {"select": {"name": data['gender']}},
            "date_of_birth": {"date": {"start": data['date_of_birth']}},
            "city": {"rich_text": [{"text": {"content": data['city']}}]},
            "is_active": {"checkbox": True},
        }
        return self.create_page(self.db_id, properties)

    def get_all_patients(self):
        return self.query_database(self.db_id)