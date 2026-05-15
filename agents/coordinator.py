import google.generativeai as genai
from config.gemini_key import GEMINI_API_KEY
from modules.system_tools import open_application, open_website, chrome_search, control_volume, power_control, open_folder
from modules.web_tools import web_search, fetch_latest_ai_news, summarize_url
from database.memory_manager import MemoryManager
from automation.screen_capture import analyze_screen

# Configure Gemini for Tool Use
genai.configure(api_key=GEMINI_API_KEY)

class CoordinatorAgent:
    def __init__(self):
        self.memory = MemoryManager()

        # Tools available to the agent, including memory tools
        self.tools = [
            open_application,
            open_website,
            chrome_search,
            control_volume,
            power_control,
            open_folder,
            web_search,
            fetch_latest_ai_news,
            summarize_url,
            self.memory.store_memory,
            self.memory.retrieve_memory,
            analyze_screen
        ]

        # Fetch initial context
        context = self.memory.get_all_context()

        system_prompt = (
            "You are JARVIS, an advanced autonomous desktop AI assistant. "
            "You have access to a variety of tools to control the system, navigate the web, fetch information, manage long-term memory, and even see the user's screen. "
            "When asked to perform a task, use the appropriate tools. If multiple steps are required, plan them out and use the tools sequentially. "
            "Always be polite, concise, and professional, like Iron Man's assistant.\n\n"
            f"{context}"
        )

        self.model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            tools=self.tools,
            system_instruction=system_prompt
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def handle(self, user_input: str) -> str:
        """
        Processes user input by passing it to the Gemini chat session.
        The `enable_automatic_function_calling=True` flag handles tool execution loops automatically.
        """
        try:
            response = self.chat.send_message(user_input)
            return response.text.strip()
        except Exception as e:
            return f"I encountered an error while processing that request, sir: {str(e)}"
