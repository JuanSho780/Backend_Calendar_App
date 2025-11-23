from pydantic import BaseModel, Field

class CalendarLLMOutputSchema(BaseModel):
    start_day: int = Field(..., description="Day of the month that is going to start the event")
    start_month: int = Field(..., description="Month of the year that is going to start the event")
    start_year: int = Field(..., description="Year that is going to start the event")
    start_hour: int = Field(..., description="Hour of the day that is going to start the event")
    start_minute: int = Field(..., description="Minute of the hour that is going to start the event")

    end_day: int = Field(..., description="Day of the month that is going to end the event")
    end_month: int = Field(..., description="Month of the year that is going to end the event")
    end_year: int = Field(..., description="Year that is going to end the event")
    end_hour: int = Field(..., description="Hour of the day that is going to end the event")
    end_minute: int = Field(..., description="Minute of the hour that is going to end the event")

    event_title: str = Field(..., description="Title of the calendar event")
    event_description: str = Field(..., description="Description of the calendar event")
    event_location: str = Field(..., description="Location of the calendar event (Here ALWAYS PUT: The location you prefer)")