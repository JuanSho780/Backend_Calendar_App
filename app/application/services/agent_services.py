from app.application.ReActAgent.agent import ReactAgent

from app.domain.value_objects.agent_output_schema import AgentOutputSchema

from app.domain.apis.gemini_client import GeminiClient
from app.domain.tools.create_event_time_tool import CreateEventTimeTool

class AgentServices:
    def __init__(self, gemini_client: GeminiClient, create_event_time_tool: CreateEventTimeTool):
        self.react_Agent = ReactAgent.get_instance(
            gemini_client=gemini_client,
            create_event_time_tool=create_event_time_tool
        )

    def run_agent(self, query: str) -> AgentOutputSchema:
        response = self.react_Agent.app.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )

        print(f"Agent Raw Response {response}")

        try:
            response_final = response["messages"][-1].content[0]["text"]
        except (AttributeError, KeyError, TypeError, IndexError):
            response_final = response["messages"][-1].content

        return AgentOutputSchema(response=response_final)