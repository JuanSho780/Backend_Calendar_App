from app.domain.repositories.event_repository import EventRepository
from app.domain.entities.Event import Event
from typing import List, Optional
from app.domain.value_objects.create_event_schema import CreateEventSchema
from app.infrastructure.database.db_connection_factory import DBConnectionFactory # for db connection
from fastapi import HTTPException

class EventRepositoryImpl(EventRepository):

    def get_all_events_by_calendar(self, calendar_id: int) -> List[Event]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, title, description, location, calendar_id FROM events WHERE calendar_id = %s", (calendar_id,))
                events_data = cursor.fetchall()
                return [
                    Event(
                        id=event[0],
                        title=event[1],
                        description=event[2],
                        location=event[3],
                        calendar_id=event[4]
                    ) for event in events_data
                ]
        finally:
            DBConnectionFactory.release_connection(connection)

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, title, description, location, calendar_id FROM events WHERE id = %s", (event_id,))
                event_data = cursor.fetchone()
                if event_data:
                    return Event(
                        id=event_data[0],
                        title=event_data[1],
                        description=event_data[2],
                        location=event_data[3],
                        calendar_id=event_data[4]
                    )
                else:
                    raise HTTPException(status_code=404, detail="Event not found")
        finally:
            DBConnectionFactory.release_connection(connection)

    def create_event(self, event: CreateEventSchema) -> Event:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO events (title, description, location, calendar_id) VALUES (%s, %s, %s, %s) RETURNING id",
                    (event.title, event.description, event.location, event.calendar_id)
                )
                event_id = cursor.fetchone()[0]
                connection.commit()
                return Event(
                    id=event_id,
                    title=event.title,
                    description=event.description,
                    location=event.location,
                    calendar_id=event.calendar_id
                )
        finally:
            DBConnectionFactory.release_connection(connection)

    def update_event(self, event_id: int, event: Event) -> Optional[Event]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE events SET title = %s, description = %s, location = %s, calendar_id = %s WHERE id = %s",
                    (event.title, event.description, event.location, event.calendar_id, event_id)
                )
                connection.commit()
                return event
        finally:
            DBConnectionFactory.release_connection(connection)

    def delete_event(self, event_id: int) -> bool:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            DBConnectionFactory.release_connection(connection)