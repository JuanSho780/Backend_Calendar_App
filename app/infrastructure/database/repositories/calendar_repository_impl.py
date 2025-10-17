from app.domain.repositories.calendar_repository import CalendarRepository
from app.domain.entities.Calendar import Calendar
from typing import List, Optional
from app.domain.value_objects.create_calendar_schema import CreateCalendarSchema
from app.infrastructure.database.db_connection_factory import DBConnectionFactory # for db connection
from fastapi import HTTPException

class CalendarRepositoryImpl(CalendarRepository):

    def get_all_calendars_by_user(self, user_id: int) -> List[Calendar]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, description, color, user_id FROM calendars WHERE user_id = %s", (user_id,))
                calendars_data = cursor.fetchall()
                return [
                    Calendar(
                        id=calendar[0],
                        name=calendar[1],
                        description=calendar[2],
                        color=calendar[3],
                        user_id=calendar[4]
                    ) for calendar in calendars_data
                ]
        finally:
            DBConnectionFactory.release_connection(connection)

    def get_calendar_by_id(self, calendar_id: int) -> Optional[Calendar]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, description, color, user_id FROM calendars WHERE id = %s", (calendar_id,))
                calendar_data = cursor.fetchone()
                if calendar_data:
                    return Calendar(
                        id=calendar_data[0],
                        name=calendar_data[1],
                        description=calendar_data[2],
                        color=calendar_data[3],
                        user_id=calendar_data[4]
                    )
                else:
                    raise HTTPException(status_code=404, detail="Calendar not found")
        finally:
            DBConnectionFactory.release_connection(connection)

    def create_calendar(self, calendar: CreateCalendarSchema) -> Calendar:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO calendars (name, description, color, user_id) VALUES (%s, %s, %s, %s) RETURNING id",
                    (calendar.name, calendar.description, calendar.color, calendar.user_id)
                )
                calendar_id = cursor.fetchone()[0]
                connection.commit()
                return Calendar(
                    id=calendar_id,
                    name=calendar.name,
                    description=calendar.description,
                    color=calendar.color,
                    user_id=calendar.user_id
                )
        finally:
            DBConnectionFactory.release_connection(connection)

    def update_calendar(self, calendar_id: int, calendar: Calendar) -> Optional[Calendar]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE calendars SET name = %s, description = %s, color = %s, user_id = %s WHERE id = %s",
                    (calendar.name, calendar.description, calendar.color, calendar.user_id, calendar_id)
                )
                connection.commit()
                return calendar
        finally:
            DBConnectionFactory.release_connection(connection)

    def delete_calendar(self, calendar_id: int) -> bool:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM calendars WHERE id = %s", (calendar_id,))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            DBConnectionFactory.release_connection(connection)