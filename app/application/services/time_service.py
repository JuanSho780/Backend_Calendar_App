from fastapi import HTTPException

from app.domain.repositories.time_repository import TimeRepository
from app.domain.apis.apscheduler_back import AppSchedulerBack
from app.domain.apis.mail_sending_api import MailSendingAPI

from app.domain.entities.Time import Time
from app.domain.value_objects.create_time_schema import CreateTimeSchema

from datetime import datetime, timedelta

class TimeService:
    def __init__(self, time_repository: TimeRepository, scheduler: AppSchedulerBack, mail_api: MailSendingAPI): # Dependency Injection
        self.time_repository = time_repository
        self.scheduler = scheduler
        self.mail_api = mail_api

    def get_all_times_by_event(self, event_id: int) -> list[Time]:
        return self.time_repository.get_all_times_by_event(event_id)
    
    def get_time_by_id(self, time_id: int) -> Time:
        return self.time_repository.get_time_by_id(time_id)

    def create_time(self, time: CreateTimeSchema, user_email: str, user_name: str, event_name: str) -> Time:
        return_time = self.time_repository.create_time(time)

        try:
            init_native_time = return_time.start_time.to_native()
            notification_hour = init_native_time - timedelta(minutes=5)

            # Asunto con un emoji para resaltar en la bandeja de entrada
            subject = f"🔔 Starting in 5 min: {event_name}"

            # Contenido HTML estructurado
            content = f"""
            <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px; background-color: #ffffff;">
                
                <div style="text-align: center; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 20px;">
                    <h2 style="color: #333; margin: 0;">Upcoming Event 📅</h2>
                </div>

                <p style="font-size: 16px; color: #555;">Hello <strong>{user_name}</strong>,</p>

                <p style="font-size: 16px; color: #555; line-height: 1.5;">
                    Just a quick heads-up! Your next event is scheduled to begin in exactly <span style="color: #d9534f; font-weight: bold;">5 minutes</span>.
                </p>

                <div style="background-color: #f9f9f9; border-left: 4px solid #007bff; padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <h3 style="margin: 0; color: #2c3e50; font-size: 18px;">{event_name}</h3>
                    <p style="margin: 5px 0 0; color: #777; font-size: 14px;">
                        ⏰ Starts at: {init_native_time.strftime('%H:%M')} ({init_native_time.strftime('%Y-%m-%d')})
                    </p>
                </div>

                <p style="font-size: 16px; color: #555;">Make sure you are ready!</p>
                
                <br>
                
                <div style="border-top: 1px solid #eee; padding-top: 20px; color: #888; font-size: 14px;">
                    Your assistant,<br>
                    <strong style="color: #007bff; font-size: 16px;">PlanifyMe</strong>
                </div>

            </div>
            """

            if notification_hour > datetime.now():
                self.scheduler.add_job(
                    self.mail_api.send_notification_email,
                    'date', 
                    run_date=notification_hour, 
                    args=[user_email, subject, content], 
                    id=f"notif_event_{time.event_id}_time_{return_time.id}" # ID único
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to schedule notification email: {str(e)}")
        
        return return_time

    def update_time(self, time_id: int, time: Time) -> Time:
        return self.time_repository.update_time(time_id, time)

    def delete_time(self, time_id: int) -> bool:
        return self.time_repository.delete_time(time_id)