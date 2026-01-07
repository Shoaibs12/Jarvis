import os
import google.generativeai as genai
from config.gemini_key import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("models/gemini-2.5-flash")


# -------------------------------------------------------------
# SAFE TEXT EXTRACTOR
# -------------------------------------------------------------
def safe_extract(response):
    """Safely extract text from Gemini response without crashes."""
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        if response.candidates:
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text.strip()

    except:
        pass

    return "I could not generate a valid response."


# -------------------------------------------------------------
# CODE AGENT
# -------------------------------------------------------------
class CodeAgent:

    # ---------------------------------------------------------
    # GENERATE PYTHON CODE
    # ---------------------------------------------------------
    def generate_code(self, prompt):
        try:
            response = MODEL.generate_content(
                f"""
Generate clean, optimized, error-free Python code.

Instructions:
- ONLY return Python code.
- Do NOT return explanations unless necessary.
- Avoid markdown like ```python``` in the output.

User request:
{prompt}
"""
            )
            return safe_extract(response)

        except Exception as e:
            return f"Gemini error while generating code: {str(e)}"

    # ---------------------------------------------------------
    # EXPLAIN CODE
    # ---------------------------------------------------------
    def explain_code(self, code):
        try:
            response = MODEL.generate_content(
                f"""
Explain the following Python code step-by-step in simple language.
Do NOT add extra assumptions.

Code:
{code}
"""
            )
            return safe_extract(response)

        except Exception as e:
            return f"Gemini error while explaining code: {str(e)}"

    # ---------------------------------------------------------
    # FIX BROKEN CODE
    # ---------------------------------------------------------
    def fix_code(self, code, error_message=None):
        error_message = error_message or "Unknown error"

        try:
            response = MODEL.generate_content(
                f"""
Fix the following Python code. Provide ONLY corrected code.
Do NOT include markdown like ```python```.

Error message:
{error_message}

Broken code:
{code}
"""
            )
            return safe_extract(response)

        except Exception as e:
            return f"Gemini error while fixing code: {str(e)}"

    # ---------------------------------------------------------
    # SAVE GENERATED FILE
    # ---------------------------------------------------------
    def save_file(self, filename, content):
        try:
            directory = "generated_code"
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, filename)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            return f"File successfully saved at: {path}"

        except Exception as e:
            return f"Could not save file: {str(e)}"
