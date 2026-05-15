import requests
import json
import os

class LibreChatClient:
    """
    Client for interacting with the LibreChat backend APIs.
    """
    def __init__(self, base_url="http://localhost:3080/api/v1", api_key=None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.environ.get("LIBRECHAT_API_KEY", "")

    def chat_completion(self, messages, model="gpt-4o", temperature=0.7):
        """
        Calls the LibreChat chat completions endpoint.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": False
        }

        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            return f"LibreChat API Error: {str(e)}"
