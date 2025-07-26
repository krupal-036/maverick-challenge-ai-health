from .base_service import NotionService
from django.conf import settings
import uuid
import bcrypt
from datetime import datetime

class DoctorService(NotionService):
    def __init__(self):
        super().__init__()
        self.db_id = settings.NOTION_DOCTOR_DB_ID

    def find_doctor_by_email(self, email):
        filter_data = {"property": "email", "email": {"equals": email}}
        results = self.query_database(self.db_id, filter_data)
        return results[0] if results else None

    def create_doctor(self, data):
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        properties = {
            "id": {"title": [{"text": {"content": str(uuid.uuid4())}}]},
            "full_name": {"rich_text": [{"text": {"content": data['full_name']}}]},
            "email": {"email": data['email']},
            "password_hash": {"rich_text": [{"text": {"content": hashed_password}}]},
            "phone_number": {"phone_number": data['phone_number']},
            "medical_registration_number": {"rich_text": [{"text": {"content": data['medical_registration_number']}}]},
            "specialization": {"select": {"name": data['specialization']}},
            "experience_years": {"number": int(data['experience_years'])},
            "city": {"rich_text": [{"text": {"content": data['city']}}]},
            "bio": {"rich_text": [{"text": {"content": data['bio']}}]},
            "is_approved": {"checkbox": False},
            "is_active": {"checkbox": True},
        }
        return self.create_page(self.db_id, properties)

    def get_all_doctors(self, approved_only=False):
        filters = []
        if approved_only:
            filters.append({"property": "is_approved", "checkbox": {"equals": True}})
        
        filter_data = {"and": filters} if filters else None
        return self.query_database(self.db_id, filter_data)
        
    def approve_doctor_account(self, page_id):
        return self.update_page(page_id, {"is_approved": {"checkbox": True}})