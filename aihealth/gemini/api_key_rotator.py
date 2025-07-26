import threading
from django.conf import settings

class ApiKeyRotator:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.keys = settings.GEMINI_API_KEYS
                cls._instance.current_key_index = 0
        return cls._instance

    def get_key(self):
        with self._lock:
            key = self.keys[self.current_key_index]
            return key

    def rotate_key(self):
        with self._lock:
            self.current_key_index = (self.current_key_index + 1) % len(self.keys)
            if self.current_key_index == 0:
                return None
            return self.keys[self.current_key_index]