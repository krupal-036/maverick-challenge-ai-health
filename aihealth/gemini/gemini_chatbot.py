from google import genai
from .api_key_rotator import ApiKeyRotator

class GeminiChatbot:
    def __init__(self):
        self.key_rotator = ApiKeyRotator()

    def get_diagnosis(self, symptoms):
        initial_key = self.key_rotator.get_key()
        
        while True:
            current_key = self.key_rotator.get_key()
            try:
                # NEW: Initialize the Client
                client = genai.Client(api_key=current_key)
                
                # UPDATED: Added 'models/' prefix to the model name
                response = client.models.generate_content(
                    model='models/gemini-3-flash-preview', 
                    contents=f"""
                    Analyze the following patient symptoms and provide a potential diagnosis and recommendations.
                    Structure the response in two parts: 'Potential Diagnosis' and 'Recommendations'.
                    Be concise and clear. This is for informational purposes and not a substitute for professional medical advice.
                    Symptoms: "{symptoms}"
                    """
                )
                
                return response.text

            except Exception as e:
                print(f"Gemini API error with key {current_key[:5]}...: {e}")
                next_key = self.key_rotator.rotate_key()
                if next_key is None or next_key == initial_key:
                    return "Error: The AI service is currently unavailable. All API keys have failed. Please try again later."