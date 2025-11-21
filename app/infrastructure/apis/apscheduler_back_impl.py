from app.domain.apis.apscheduler_back import AppSchedulerBack

from dotenv import load_dotenv
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from sqlalchemy import create_engine

class AppSchedulerBackImpl(AppSchedulerBack):
    _instance = None

    @classmethod
    def initialize(cls,):
        load_dotenv()

        PASSWORD = os.getenv("DB_PASSWORD")
        HOST = os.getenv("DB_HOST")
        PORT = os.getenv("DB_PORT")
        DBNAME = os.getenv("DB_NAME")

        postgres_url = f"postgresql+psycopg2://postgres:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

        engine = create_engine(
            postgres_url,
            pool_pre_ping=True,
        )

        jobstores = {
            'default': SQLAlchemyJobStore(engine=engine)
        }

        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }

        job_defaults = {
            'coalesce': False, 
            'max_instances': 1
        }

        if cls._instance is None:
            cls._instance = BackgroundScheduler(
                jobstores=jobstores,
                executors=executors,
                job_defaults=job_defaults,
                timezone="America/Lima"
            )
            cls._instance.start()
        return cls._instance

    @classmethod
    def get_scheduler(cls):
        if cls._instance is None:
            raise Exception("AppScheduler is not initialized")
        return cls._instance
    
    def saveCreatedTime(self, method,run_date, job_id) -> None:
        scheduler = self.initialize()
        scheduler.add_job(
            method,
            'date',
            run_date=run_date,
            id=job_id,
            replace_existing=True
        )