import google.generativeai as genai
from .api_key_rotator import ApiKeyRotator

class GeminiChatbot:
    def __init__(self):
        self.key_rotator = ApiKeyRotator()

    def get_diagnosis(self, symptoms):
        initial_key = self.key_rotator.get_key()
        
        while True:
            current_key = self.key_rotator.get_key()
            try:
                genai.configure(api_key=current_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Analyze the following patient symptoms and provide a potential diagnosis and recommendations.
                Structure the response in two parts: 'Potential Diagnosis' and 'Recommendations'.
                Be concise and clear. This is for informational purposes and not a substitute for professional medical advice.
                Symptoms: "{symptoms}"
                """
                
                response = model.generate_content(prompt)
                return response.text

            except Exception as e:
                print(f"Gemini API error with key {current_key[:5]}...: {e}")
                next_key = self.key_rotator.rotate_key()
                if next_key is None or next_key == initial_key:
                    return "Error: The AI service is currently unavailable. All API keys have failed. Please try again later."