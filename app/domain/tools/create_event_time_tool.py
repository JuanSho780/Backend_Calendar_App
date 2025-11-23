from abc import ABC, abstractmethod

class CreateEventTimeTool(ABC):
    @abstractmethod
    def create_event_time(self, llm_response_prev: str, calendar_id: int, user_email: str, user_name: str) -> str:
        pass