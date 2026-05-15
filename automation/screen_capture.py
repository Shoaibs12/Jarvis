import pyautogui
from PIL import Image
import io
import base64
from ai.librechat_client import LibreChatClient

def analyze_screen(prompt: str = "Describe what is on my screen in detail.") -> str:
    """
    Takes a screenshot of the user's desktop and asks the LibreChat vision model to analyze it.
    """
    try:
        screenshot = pyautogui.screenshot()

        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
            }
        ]

        client = LibreChatClient()
        response = client.chat_completion(messages, model="gpt-4o")
        return response.strip()
    except Exception as e:
        return f"Failed to capture or analyze screen: {str(e)}"
