from app.domain.tools.create_event_time_tool import CreateEventTimeTool
from app.domain.structured_schemas.calendar_llm_out_schema import CalendarLLMOutputSchema

from app.application.services.event_service import EventService
from app.application.services.time_service import TimeService

from app.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from app.infrastructure.database.repositories.time_repository_impl import TimeRepositoryImpl

from app.infrastructure.apis.apscheduler_back_impl import AppSchedulerBackImpl
from app.infrastructure.apis.mail_sending_api_impl import MailSendingAPIImpl

from typing import Any, Dict, Optional, List

from app.infrastructure.apis.gemini_client_impl import GeminiClientImpl

from app.domain.value_objects.create_event_schema import CreateEventSchema
from app.domain.value_objects.create_time_schema import CreateTimeSchema
from app.domain.value_objects.date_time import DateTime

def get_event_service():
    repository = EventRepositoryImpl()
    return EventService(repository) #dependency injection

def get_time_service():
    repository = TimeRepositoryImpl()
    scheduler = AppSchedulerBackImpl.get_scheduler()
    mail_api = MailSendingAPIImpl()
    return TimeService(repository, scheduler, mail_api) #dependency injection

class CreateEventTimeToolImpl(CreateEventTimeTool):
    def create_event_time(self, llm_response_prev: str, calendar_id: int, user_email: str, user_name: str) -> str:
        gemini_client = GeminiClientImpl.get_instance()
        
        my_schema = CalendarLLMOutputSchema
        response_structured_event_time = gemini_client.generate_event_time_structured(query=llm_response_prev, response_schema=my_schema)

        event_service = get_event_service()
        time_service = get_time_service()

        new_event = CreateEventSchema(
            title=response_structured_event_time['event_title'],
            description=response_structured_event_time['event_description'],
            location=response_structured_event_time['event_location'],
            calendar_id=calendar_id
        )
        
        event_created = event_service.create_event(new_event)

        init_datetime = DateTime(
            day=response_structured_event_time['start_day'],
            month=response_structured_event_time['start_month'],
            year=response_structured_event_time['start_year'],
            hour=response_structured_event_time['start_hour'],
            minute=response_structured_event_time['start_minute']
        )

        end_datetime = DateTime(
            day=response_structured_event_time['end_day'],
            month=response_structured_event_time['end_month'],
            year=response_structured_event_time['end_year'],
            hour=response_structured_event_time['end_hour'],
            minute=response_structured_event_time['end_minute']
        )

        new_time = CreateTimeSchema(
            start_time=init_datetime,
            end_time=end_datetime,
            event_id=event_created.id
        )

        time_service.create_time(
            time=new_time,
            user_email=user_email,
            user_name=user_name,
            event_name=event_created.title
        )

        return "Event and its time created succesfully"