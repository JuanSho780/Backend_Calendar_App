from fastapi import HTTPException

from app.domain.apis.gemini_client import GeminiClient
from typing import Type

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage

from app.domain.structured_schemas.calendar_llm_out_schema import CalendarLLMOutputSchema

class GeminiClientImpl(GeminiClient):
    _client_instance = None
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        try:
            self.model_name = model_name

            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=0.7,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize GeminiClient: {str(e)}")
        
    @classmethod
    def get_instance(cls, model_name: str = "gemini-2.5-flash"):
        if cls._client_instance is None:
            print("Creating GeminiClient for the first time")
            cls._client_instance = cls(model_name=model_name)
        return cls._client_instance
    
    def get_model(self):
        return self.llm
    
    def generate_event_time_structured(self, query: str, response_schema: Type[CalendarLLMOutputSchema]) -> CalendarLLMOutputSchema:
        try:
            structured_llm = self.llm.with_structured_output(response_schema)
            system_prompt = """
            Your are an expert information extractor about a task (create event task) that is gived to you.
            Please be precise with all information you retrieve.
            """

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ]
            result_object = structured_llm.invoke(messages)
            return result_object.model_dump()
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get structured response by Gemini model: {str(e)}")