from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.routers.user_router import router as user_router
from app.infrastructure.routers.calendar_router import router as calendar_router
from app.infrastructure.routers.event_router import router as event_router
from app.infrastructure.routers.time_router import router as time_router
from app.infrastructure.routers.agent_router import router as agent_router

from app.infrastructure.database.db_connection_factory import DBConnectionFactory

from app.infrastructure.apis.apscheduler_back_impl import AppSchedulerBackImpl
from app.infrastructure.apis.gemini_client_impl import GeminiClientImpl
from app.application.ReActAgent.agent import ReactAgent
from app.infrastructure.tools.create_event_time_tool_impl import CreateEventTimeToolImpl

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:3001/",
    "http://localhost:3002"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    print("Starting up connection pool...")
    DBConnectionFactory.initialize()

    print("Starting scheduler...")
    AppSchedulerBackImpl.initialize()

    print("Starting Gemini LLM...")
    GeminiClientImpl.get_instance()

    print("Starting ReAct Agent...")
    ReactAgent.get_instance(
        gemini_client=GeminiClientImpl.get_instance(),
        create_event_time_tool=CreateEventTimeToolImpl()
    )

@app.on_event("shutdown")
def shutdown():
    print("Shutting down connection pool...")
    DBConnectionFactory.close_pool()
    AppSchedulerBackImpl.get_scheduler().shutdown()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(calendar_router, prefix="/calendars", tags=["calendars"])
app.include_router(event_router, prefix="/events", tags=["events"])
app.include_router(time_router, prefix="/times", tags=["times"])
app.include_router(agent_router, prefix="/agent", tags=["agent"])