import google.generativeai as genai
from config.gemini_key import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

classifier_model = genai.GenerativeModel("models/gemini-2.5-flash")


class TaskClassifier:

    def classify(self, text: str):
        """
        Uses Gemini to classify the text into:
        - code_task
        - web_search
        - system_control
        - general_question
        """

        prompt = f"""
You are an intelligent intent-classification model for a JARVIS AI assistant.

Classify the user message into EXACTLY ONE of these categories:

1. code_task  → Anything related to coding, programming, generating code, fixing code, explaining code  
2. web_search → If the user wants information from the internet, news, lookup, search, weather, etc.  
3. system_control → If the user wants to control the computer. 
Examples: open app, open website, volume control, brightness, shutdown, restart, sleep, folders, calculator, chrome, vs code  
4. general_question → General questions, opinions, explanations, knowledge queries.

Return ONLY the category name. No extra text.

User message:
"{text}"
"""

        try:
            response = classifier_model.generate_content(prompt)
            category = response.text.strip().lower()

            # Safety normalization
            valid = ["code_task", "web_search", "system_control", "general_question"]
            return category if category in valid else "general_question"

        except Exception as e:
            print("Classifier LLM Error:", e)
            return "general_question"
