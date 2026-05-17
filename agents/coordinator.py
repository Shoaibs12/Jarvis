from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List, Union
import operator
from ai.model_router import ModelRouter
from database.memory_manager import MemoryManager
from modules.system_tools import open_application, open_website, chrome_search, control_volume, power_control, open_folder
from modules.web_tools import web_search, fetch_latest_ai_news, summarize_url
from automation.screen_capture import analyze_screen
from automation.browser_agent import browser_navigate, browser_click, browser_type, browser_read
import json

class AgentState(TypedDict):
    input: str
    messages: Annotated[List[str], operator.add]
    tools_called: Annotated[List[str], operator.add]
    final_response: str

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
            "analyze_screen": analyze_screen,
            "browser_navigate": browser_navigate,
            "browser_click": browser_click,
            "browser_type": browser_type,
            "browser_read": browser_read
        }

        self.graph = self._build_graph()

    def _get_system_prompt(self):
        context = self.memory.get_all_context()
        tool_descriptions = "\n".join([f"- {name}" for name in self.tools_map.keys()])

        return (
            "You are JARVIS, an autonomous multimodal AI operating assistant. "
            "You use LibreChat to access models. "
            f"Available tools: \n{tool_descriptions}\n\n"
            "If you need to use a tool, return ONLY a JSON object: "
            '{"tool": "tool_name", "args": ["arg1", "arg2"]}. '
            "If you have the final answer, return the text directly without JSON.\n"
            f"{context}"
        )

    def _planner_node(self, state: AgentState):
        system_prompt = self._get_system_prompt()
        prompt = state["input"]
        if state["messages"]:
            prompt += "\n\nHistory: " + " | ".join(state["messages"])

        response = self.router.route_request(prompt, system_prompt=system_prompt)

        try:
            # Look for JSON tool call
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                tool_data = json.loads(json_str)
                if "tool" in tool_data:
                    return {"messages": [response], "final_response": response}
        except:
            pass

        return {"messages": [response], "final_response": response}

    def _executor_node(self, state: AgentState):
        last_msg = state["messages"][-1]
        try:
            start = last_msg.find("{")
            end = last_msg.rfind("}") + 1
            json_str = last_msg[start:end]
            tool_data = json.loads(json_str)

            tool_name = tool_data.get("tool")
            args = tool_data.get("args", [])

            if tool_name in self.tools_map:
                print(f"[JARVIS] Executing {tool_name} with {args}...")
                result = self.tools_map[tool_name](*args)
                return {"messages": [f"Tool {tool_name} returned: {result}"], "tools_called": [tool_name]}
        except Exception as e:
            return {"messages": [f"Tool execution failed: {e}"]}

        return {"messages": ["Failed to parse tool JSON."]}

    def _should_continue(self, state: AgentState) -> str:
        last_msg = state["messages"][-1]
        try:
            if "{" in last_msg and "}" in last_msg and "tool" in json.loads(last_msg[last_msg.find("{"):last_msg.rfind("}")+1]):
                return "execute"
        except:
            pass
        return "end"

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("planner", self._planner_node)
        workflow.add_node("executor", self._executor_node)

        workflow.add_edge(START, "planner")
        workflow.add_conditional_edges(
            "planner",
            self._should_continue,
            {
                "execute": "executor",
                "end": END
            }
        )
        workflow.add_edge("executor", "planner")

        return workflow.compile()

    def handle(self, user_input: str) -> str:
        """
        Invokes the LangGraph state machine.
        """
        try:
            initial_state = {"input": user_input, "messages": [], "tools_called": [], "final_response": ""}
            result = self.graph.invoke(initial_state)
            return result.get("final_response", "I could not formulate a response.")
        except Exception as e:
            return f"I encountered an orchestration error, sir: {str(e)}"
