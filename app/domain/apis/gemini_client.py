from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from app.domain.structured_schemas.calendar_llm_out_schema import CalendarLLMOutputSchema

class GeminiClient(ABC):    
    @abstractmethod
    def generate_event_time_structured(self, query: str, response_schema: Type[CalendarLLMOutputSchema]) -> CalendarLLMOutputSchema:
        pass

    @abstractmethod
    def get_model(self):
        pass