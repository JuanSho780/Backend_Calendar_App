from fastapi import APIRouter, status, HTTPException, Depends
from app.application.services.agent_services import AgentServices

from app.domain.value_objects.agent_output_schema import AgentOutputSchema
from app.domain.value_objects.agent_input_schema import AgentInputSchema

from app.infrastructure.tools.create_event_time_tool_impl import CreateEventTimeToolImpl

from app.infrastructure.apis.gemini_client_impl import GeminiClientImpl

from app.authentication.services.auth_service import get_current_user
from app.domain.entities.User import User

import datetime
from app.application.services.calendar_service import CalendarService
from app.application.services.event_service import EventService
from app.application.services.time_service import TimeService

from app.infrastructure.apis.mail_sending_api_impl import MailSendingAPIImpl
from app.infrastructure.apis.apscheduler_back_impl import AppSchedulerBackImpl

from app.infrastructure.database.repositories.calendar_repository_impl import CalendarRepositoryImpl
from app.infrastructure.database.repositories.event_repository_impl import EventRepositoryImpl
from app.infrastructure.database.repositories.time_repository_impl import TimeRepositoryImpl

from app.application.schemas.event_times_schema import EventTimesSchema
from app.application.schemas.calendar_events_times import CalendarEventsTimesSchema

import json

router = APIRouter()

def get_calendar_service():
    repository = CalendarRepositoryImpl()
    return CalendarService(repository) #dependency injection

def get_event_service():
    repository = EventRepositoryImpl()
    return EventService(repository) #dependency injection

def get_time_service():
    repository = TimeRepositoryImpl()
    scheduler = AppSchedulerBackImpl.get_scheduler()
    mail_api = MailSendingAPIImpl()
    return TimeService(repository, scheduler, mail_api) #dependency injection

@router.get("/")
def res_root():
    return {"message": "Hola!! Soy PlanifyMe, tu assitente personal para planear y crear horarios de acuerdo a tus necesidades. Cuéntame, ¿en qué necesitas que te ayude?"}

@router.post("/get_response", response_model=AgentOutputSchema, summary="get response from PlanifyMe AI Agent")
def get_agent_response(user: AgentInputSchema, current_user: User = Depends(get_current_user), calendar_service: CalendarService = Depends(get_calendar_service), event_service: EventService = Depends(get_event_service), time_service: TimeService = Depends(get_time_service)):
    agent_service = AgentServices(
        gemini_client=GeminiClientImpl.get_instance(),
        create_event_time_tool=CreateEventTimeToolImpl()
    )

    calendars = calendar_service.get_all_calendars_by_user(current_user.id)
    calendars_events_times = []
    for calendar in calendars:
        events = event_service.get_all_events_by_calendar(calendar.id)
        event_times = []
        for event in events:
            times = time_service.get_all_times_by_event(event.id)
            event_times.append(EventTimesSchema(id_calendar=event.calendar_id, event=event, times=times))
        calendars_events_times.append(CalendarEventsTimesSchema(calendar=calendar, events_times=event_times))

    str_calendars_events_times = [item.model_dump() for item in calendars_events_times]
    actual_query = user.user_query + f". MY PERSONAL INFORMATION: calendar_id: {current_user.planifyme_calendar_id}, user_email: {current_user.email}, user_name: {current_user.name}, the current hour is: {datetime.datetime.now()} and my current schedule is this {json.dumps(str_calendars_events_times, indent=4, default=str)}"
    response = agent_service.run_agent(query=actual_query)

    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return response