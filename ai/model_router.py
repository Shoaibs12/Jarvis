import re
from ai.librechat_client import LibreChatClient

class ModelRouter:
    """
    Intelligently routes tasks to the most appropriate model via the LibreChat backend.
    """
    def __init__(self, fallback_model="gemini-2.5-flash"):
        self.client = LibreChatClient()
        self.fallback_model = fallback_model

        # Route mapping definitions
        self.routes = {
            "coding": ["code", "script", "python", "javascript", "react", "debug", "error", "terminal", "github"],
            "reasoning": ["plan", "think", "analyze", "why", "how", "solve"],
            "vision": ["see", "screen", "look", "image", "photo"],
            "offline": ["offline", "local", "private"]
        }

    def detect_task_type(self, user_input: str) -> str:
        """Analyzes the user input to determine the task type."""
        text = user_input.lower()

        for category, keywords in self.routes.items():
            if any(re.search(rf"\b{kw}\b", text) for kw in keywords):
                return category

        return "casual"

    def select_model(self, task_type: str) -> str:
        """Selects the best model based on the task type."""
        if task_type == "coding":
            return "deepseek-coder"
        elif task_type == "reasoning":
            return "gpt-4o"
        elif task_type == "vision":
            return "gemini-2.5-flash"
        elif task_type == "offline":
            return "ollama-llama3"
        else:
            return self.fallback_model

    def route_request(self, user_input: str, system_prompt: str = "") -> str:
        """
        Determines the optimal model and executes the request via LibreChat.
        """
        task_type = self.detect_task_type(user_input)
        model = self.select_model(task_type)

        print(f"🔄 [ModelRouter] Routing task '{task_type}' to model: {model}")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_input})

        return self.client.chat_completion(messages, model=model)
