import google.generativeai as genai
from config.gemini_key import GEMINI_API_KEY

from agents.task_classifier import TaskClassifier
from agents.code_agent import CodeAgent
from agents.web_agent import WebAgent
from agents.system_agent import SystemAgent

# Gemini LLM
genai.configure(api_key=GEMINI_API_KEY)
LLM = genai.GenerativeModel("models/gemini-2.5-flash")


def safe_extract(response):
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        if response.candidates:
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text.strip()
    except:
        pass
    return "I'm not sure how to respond to that, sir."


class CoordinatorAgent:

    def __init__(self):
        self.classifier = TaskClassifier()
        self.code = CodeAgent()
        self.web = WebAgent()
        self.system = SystemAgent()

    def handle(self, text: str):

        # 1. CLASSIFY USING GEMINI
        task = self.classifier.classify(text)
        lower = text.lower()

        # --------------------------
        #   CODE TASKS  
        # --------------------------
        if task == "code_task":
            if "explain" in lower:
                return self.code.explain_code(text)
            if "fix" in lower or "debug" in lower:
                return "Please provide the code and the error message, sir."

            return self.code.generate_code(text)

        # --------------------------
        #   WEB SEARCH
        # --------------------------
        if task == "web_search":
            return self.web.search(text)

        # --------------------------
        #   SYSTEM CONTROL
        # --------------------------
        if task == "system_control":

            # OPEN APP
            if "open" in lower and ("chrome" in lower or "calculator" in lower or "vs code" in lower or "notepad" in lower):
                return self.system.open_app(lower)

            # OPEN WEBSITE
            if "open" in lower or "website" in lower:
                return self.system.open_website(lower)

            # VOLUME
            if "volume" in lower or "mute" in lower:
                return self.system.control_volume(lower)

            # BRIGHTNESS
            if "brightness" in lower:
                return self.system.set_brightness(lower)

            # FOLDERS
            if "folder" in lower or "downloads" in lower or "documents" in lower:
                return self.system.open_folder(lower)

            # SHUTDOWN / RESTART
            if "shutdown" in lower:
                return self.system.shutdown()
            if "restart" in lower:
                return self.system.restart()

            return "System command detected, but I couldn't understand the exact action, sir."

        # --------------------------
        # GENERAL QUESTION → LLM
        # --------------------------
        try:
            response = LLM.generate_content(f"Answer clearly:\n{text}")
            return safe_extract(response)

        except Exception as e:
            return f"Gemini Error: {str(e)}"
