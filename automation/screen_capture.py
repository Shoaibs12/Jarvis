import pyautogui
from PIL import Image
import io
import google.generativeai as genai
from config.gemini_key import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
VISION_MODEL = genai.GenerativeModel("models/gemini-2.5-flash")

def analyze_screen(prompt: str = "Describe what is on my screen in detail.") -> str:
    """
    Takes a screenshot of the user's desktop and asks the Gemini vision model to analyze it.
    Use this tool when the user asks "what is on my screen" or asks to read/see something visible.

    Args:
        prompt: The specific question or instruction regarding the screenshot content.
    """
    try:
        # Capture screen
        screenshot = pyautogui.screenshot()

        # Save to bytes
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        image_parts = [
            {
                "mime_type": "image/png",
                "data": img_byte_arr
            }
        ]

        response = VISION_MODEL.generate_content([prompt, image_parts[0]])
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        return "I could not extract meaningful text or description from the screen."
    except Exception as e:
        return f"Failed to capture or analyze screen: {str(e)}"
