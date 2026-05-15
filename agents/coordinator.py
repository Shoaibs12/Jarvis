from ai.model_router import ModelRouter
from database.memory_manager import MemoryManager
from modules.system_tools import open_application, open_website, chrome_search, control_volume, power_control, open_folder
from modules.web_tools import web_search, fetch_latest_ai_news, summarize_url
from automation.screen_capture import analyze_screen
import shlex

class CoordinatorAgent:
    def __init__(self):
        self.memory = MemoryManager()
        self.router = ModelRouter()

        self.tools_map = {
            "open_application": open_application,
            "open_website": open_website,
            "chrome_search": chrome_search,
            "control_volume": control_volume,
            "power_control": power_control,
            "open_folder": open_folder,
            "web_search": web_search,
            "fetch_latest_ai_news": fetch_latest_ai_news,
            "summarize_url": summarize_url,
            "store_memory": self.memory.store_memory,
            "retrieve_memory": self.memory.retrieve_memory,
            "analyze_screen": analyze_screen
        }

    def _get_system_prompt(self):
        context = self.memory.get_all_context()
        tool_descriptions = "\n".join([f"- {name}" for name in self.tools_map.keys()])

        return (
            "You are JARVIS, an advanced autonomous desktop AI assistant powered by LibreChat. "
            "You have access to a variety of local tools to control the system, navigate the web, and fetch information. "
            f"Available tools: \n{tool_descriptions}\n\n"
            "If the user asks you to perform an action that matches a tool, you MUST output a command block. "
            "Format: TOOL_CALL: <tool_name> \"<arg1>\" \"<arg2>\"\n"
            "Example: TOOL_CALL: store_memory \"favorite_color\" \"user likes blue\"\n"
            "Example: TOOL_CALL: web_search \"latest AI news\"\n"
            "Example: TOOL_CALL: fetch_latest_ai_news\n"
            "If no tool is needed, just reply normally.\n"
            f"{context}"
        )

    def handle(self, user_input: str) -> str:
        """
        Processes user input. Executes tool chain if LibreChat responds with a TOOL_CALL block.
        """
        try:
            system_prompt = self._get_system_prompt()
            response = self.router.route_request(user_input, system_prompt=system_prompt)

            # Simple Agentic parsing loop
            if "TOOL_CALL:" in response:
                lines = response.split('\n')
                for line in lines:
                    if line.startswith("TOOL_CALL:"):
                        # Extract tool name and args
                        # E.g. TOOL_CALL: store_memory "user name" "john"
                        parts = line.replace("TOOL_CALL:", "").strip()

                        try:
                            # Use shlex to correctly parse arguments preserving quotes
                            split_parts = shlex.split(parts)
                            tool_name = split_parts[0]
                            args = split_parts[1:]
                        except Exception:
                            # Fallback if shlex fails
                            tool_name = parts.split(' ')[0]
                            args = []

                        if tool_name in self.tools_map:
                            print(f"[JARVIS] Executing tool {tool_name} with args {args}...")

                            # Execute the tool
                            result = self.tools_map[tool_name](*args)

                            # Feed result back to LLM to get final answer
                            follow_up = f"The tool '{tool_name}' returned: {result}. Please summarize this for the user."
                            return self.router.route_request(follow_up, system_prompt=system_prompt).strip()

            return response.strip()

        except Exception as e:
            return f"I encountered an error while processing that request, sir: {str(e)}"
