from langchain.agents import create_agent

from app.domain.apis.gemini_client import GeminiClient

from langchain.tools import tool

from app.domain.tools.create_event_time_tool import CreateEventTimeTool

class ReactAgent:
    _agent_instance = None

    def __init__(self, gemini_client: GeminiClient, create_event_time_tool: CreateEventTimeTool):
        
        self.llm_model = gemini_client.get_model()

        @tool
        def create_event_time(llm_response_prev: str, calendar_id: int, user_email: str, user_name: str) -> str:
            """Create event and its time based on your indications. Input llm_response_prev should be a sentence like: Create an event that STARTS 25/11/2026 10:00 a.m. and ENDS at 12:00 p.m. and the TITLE of the event is ... and its DESCRIPTION is ...
            Then, the other inputs you can esaily extracy by the user query, you can find it in the user query by: 'calendar_id: 1, user_email: jz@gmail.com, user_name: Juan'"""
            return create_event_time_tool.create_event_time(llm_response_prev, calendar_id, user_email, user_name)
    
        system_prompt = (
            "You are PlanifyMe, and intelligent assistant that helps users (Students) to manage their schedules effectively."
            "You are an expert in calendar management and event scheduling."
            "The user is going to provide its needs, and you will plan an schedule for its needs and assist in creating and managing their calendar events accordingly."
            "You have the aaccess to the following tools:"

            "1. create_event_time: You use this tool to create an event with a specific start time, end time, title, and description based on the user's input. Just to create ONE event in the schedule."
            "If in your plan for the user, you contemplate more than one event for its needs, you need to call N times this tool."
            "The input of this tool is a indication to create an event with a specific start time, end time, title, and description based on the user's input (needs)."
        )

        self.app = create_agent(
            model = self.llm_model,
            tools = [
                create_event_time
            ],
            system_prompt=system_prompt
        )
    
    @classmethod
    def get_instance(cls, gemini_client: GeminiClient, create_event_time_tool: CreateEventTimeTool):
        if cls._agent_instance is None:
            cls._agent_instance = cls(gemini_client, create_event_time_tool)
        return cls._agent_instance