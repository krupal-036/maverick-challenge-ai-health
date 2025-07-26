from .base_service import NotionService
from django.conf import settings
import uuid
from datetime import datetime

class ConsultationService(NotionService):
    def __init__(self):
        super().__init__()
        self.db_id = settings.NOTION_CONSULTATION_DB_ID

    def create_consultation_request(self, patient_id, doctor_id, patient_name, doctor_name):
        properties = {
            "id": {"title": [{"text": {"content": str(uuid.uuid4())}}]},
            "patient_id": {"rich_text": [{"text": {"content": patient_id}}]},
            "doctor_id": {"rich_text": [{"text": {"content": doctor_id}}]},
            "patient_name": {"rich_text": [{"text": {"content": patient_name}}]},
            "doctor_name": {"rich_text": [{"text": {"content": doctor_name}}]},
            "status": {"select": {"name": "Pending"}},
            "request_date": {"date": {"start": datetime.utcnow().isoformat()}}
        }
        return self.create_page(self.db_id, properties)

    def get_consultations_for_doctor(self, doctor_page_id):
        filter_data = {
            "and": [
                {"property": "doctor_id", "rich_text": {"equals": doctor_page_id}},
                {"property": "status", "select": {"equals": "Pending"}}
            ]
        }
        return self.query_database(self.db_id, filter_data)
        
    def get_consultations_for_patient(self, patient_page_id):
        filter_data = {"property": "patient_id", "rich_text": {"equals": patient_page_id}}
        return self.query_database(self.db_id, filter_data)

    def update_consultation_status(self, request_page_id, status):
        properties = {"status": {"select": {"name": status}}}
        return self.update_page(request_page_id, properties)