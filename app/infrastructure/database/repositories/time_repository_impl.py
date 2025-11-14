from app.domain.repositories.time_repository import TimeRepository
from app.domain.entities.Time import Time
from app.domain.value_objects.create_time_schema import CreateTimeSchema
from typing import List, Optional
from app.infrastructure.database.db_connection_factory import DBConnectionFactory # for db connection
from fastapi import HTTPException
from app.domain.value_objects.date_time import DateTime

class TimeRepositoryImpl(TimeRepository):

    def get_all_times_by_event(self, event_id) -> List[Time]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, start_time_day, start_time_month, start_time_year, start_time_hour, start_time_minute, end_time_day, end_time_month, end_time_year, end_time_hour, end_time_minute, event_id FROM times WHERE event_id = %s", (event_id,))
                times_data = cursor.fetchall()
                return [
                    Time(
                        id=time[0],
                        start_time=DateTime(
                            day=time[1],
                            month=time[2],
                            year=time[3],
                            hour=time[4],
                            minute=time[5]
                        ),
                        end_time=DateTime(
                            day=time[6],
                            month=time[7],
                            year=time[8],
                            hour=time[9],
                            minute=time[10]
                        ),
                        event_id=time[11]
                    ) for time in times_data
                ]
        finally:
            DBConnectionFactory.release_connection(connection)

    def get_time_by_id(self, time_id: int) -> Optional[Time]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, start_time_day, start_time_month, start_time_year, start_time_hour, start_time_minute, end_time_day, end_time_month, end_time_year, end_time_hour, end_time_minute, event_id FROM times WHERE id = %s", (time_id,))
                time_data = cursor.fetchone()
                if time_data:
                    return Time(
                        id=time_data[0],
                        start_time=DateTime(
                            day=time_data[1],
                            month=time_data[2],
                            year=time_data[3],
                            hour=time_data[4],
                            minute=time_data[5]
                        ),
                        end_time=DateTime(
                            day=time_data[6],
                            month=time_data[7],
                            year=time_data[8],
                            hour=time_data[9],
                            minute=time_data[10]
                        ),
                        event_id=time_data[11]
                    )
                else:
                    raise HTTPException(status_code=404, detail="Time not found")
        finally:
            DBConnectionFactory.release_connection(connection)

    def create_time(self, time: Time) -> Time:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO times (start_time_day, start_time_month, start_time_year, start_time_hour, start_time_minute, end_time_day, end_time_month, end_time_year, end_time_hour, end_time_minute, event_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (time.start_time.day, time.start_time.month, time.start_time.year, time.start_time.hour, time.start_time.minute,
                     time.end_time.day, time.end_time.month, time.end_time.year, time.end_time.hour, time.end_time.minute,
                     time.event_id) # review overload of var
                )
                time_id = cursor.fetchone()[0]
                connection.commit()
                return Time(
                    id=time_id,
                    start_time=time.start_time,
                    end_time=time.end_time,
                    event_id=time.event_id
        )
        finally:
            DBConnectionFactory.release_connection(connection)

    def update_time(self, time_id: int, time: CreateTimeSchema) -> Optional[CreateTimeSchema]:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE times SET start_time_day = %s, start_time_month = %s, start_time_year = %s, start_time_hour = %s, start_time_minute = %s, end_time_day = %s, end_time_month = %s, end_time_year = %s, end_time_hour = %s, end_time_minute = %s, event_id = %s WHERE id = %s",
                    (time.start_time.day, time.start_time.month, time.start_time.year, time.start_time.hour, time.start_time.minute,
                     time.end_time.day, time.end_time.month, time.end_time.year, time.end_time.hour, time.end_time.minute,
                     time.event_id, time_id)
                )
                connection.commit()
                return time
        finally:
            DBConnectionFactory.release_connection(connection)

    def delete_time(self, time_id: int) -> bool:
        connection = DBConnectionFactory.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM times WHERE id = %s", (time_id,))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            DBConnectionFactory.release_connection(connection)