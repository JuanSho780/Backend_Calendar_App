from fastapi import APIRouter, Depends
from app.infrastructure.database.repositories.time_repository_impl import TimeRepositoryImpl
from app.application.services.time_service import TimeService
#from app.application.schemas.login_input_schema import loginInputSchema

from app.domain.value_objects.create_time_schema import CreateTimeSchema
from app.domain.entities.Time import Time
from typing import List

router = APIRouter()

def get_time_service():
    repository = TimeRepositoryImpl()
    return TimeService(repository) #dependency injection

@router.get("/")
def res_root():
    return {"message": "Welcome to the Time Router"}

@router.get("/get_all_times/{event_id}", response_model=List[Time], summary="Get all times for an event")
def get_all_times(event_id: int, time_service: TimeService = Depends(get_time_service)):
    return time_service.get_all_times_by_event(event_id)

@router.get("/get_time/{time_id}", response_model=Time, summary="Get a time by its ID")
def get_time(time_id: int, time_service: TimeService = Depends(get_time_service)):
    return time_service.get_time_by_id(time_id)

@router.post("/create_time", response_model=Time, summary="Create a new time entry")
def create_time(time: CreateTimeSchema, time_service: TimeService = Depends(get_time_service)):
    return time_service.create_time(time)

@router.put("/update_time/{time_id}", response_model=Time, summary="Update a time entry by its ID")
def update_time(time_id: int, time: Time, time_service: TimeService = Depends(get_time_service)):
    return time_service.update_time(time_id, time)

@router.delete("/delete_time/{time_id}", response_model=bool, summary="Delete a time entry by its ID")
def delete_time(time_id: int, time_service: TimeService = Depends(get_time_service)):
    return time_service.delete_time(time_id)