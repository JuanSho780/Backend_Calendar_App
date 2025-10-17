from fastapi import FastAPI
from app.infrastructure.routers.user_router import router as user_router
from app.infrastructure.routers.calendar_router import router as calendar_router
from app.infrastructure.routers.event_router import router as event_router
from app.infrastructure.routers.time_router import router as time_router

from app.infrastructure.database.db_connection_factory import DBConnectionFactory

app = FastAPI()

@app.on_event("startup")
def startup():
    print("Starting up connection pool...")
    DBConnectionFactory.initialize()

@app.on_event("shutdown")
def shutdown():
    print("Shutting down connection pool...")
    DBConnectionFactory.close_pool()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(calendar_router, prefix="/calendars", tags=["calendars"])
app.include_router(event_router, prefix="/events", tags=["events"])
app.include_router(time_router, prefix="/times", tags=["times"])