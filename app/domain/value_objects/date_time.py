from pydantic import BaseModel, Field, field_validator

from datetime import datetime

class DateTime(BaseModel):

    day: int = Field(..., description="Day of the month")
    month: int = Field(..., description="Month of the year")
    year: int = Field(..., description="Year")
    hour: int = Field(..., description="Hour of the day")
    minute: int = Field(..., description="Minute of the hour")
        
    def to_native(self) -> datetime:
        """Convierte este objeto a un datetime nativo de Python"""
        return datetime(
            self.year, self.month, self.day, self.hour, self.minute
        )
    
    @field_validator('day')
    def validate_day(cls, day):
        if not (1 <= day <= 31):
            raise ValueError("Day must be between 1 and 31")
        return day
    
    @field_validator('month')
    def validate_month(cls, month):
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12")
        return month
        
    @field_validator('year')
    def validate_year(cls, year):
        if not (1900 <= year <= 2100):
            raise ValueError("Year must be between 1900 and 2100")
        return year

    @field_validator('hour')
    def validate_hour(cls, hour):
        if not (0 <= hour <= 23):
            raise ValueError("Hour must be between 0 and 23")
        return hour

    @field_validator('minute')
    def validate_minute(cls, minute):
        if not (0 <= minute <= 59):
            raise ValueError("Minute must be between 0 and 59")
        return minute

    def __str__(self):
        return f"{self.day:02}/{self.month:02}/{self.year} {self.hour:02}:{self.minute:02}"
    
    def __eq__(self, other):
        return isinstance(other, DateTime) and self.day == other.day and self.month == other.month and self.year == other.year and self.hour == other.hour and self.minute == other.minute

