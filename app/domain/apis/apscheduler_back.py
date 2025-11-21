from abc import ABC, abstractmethod


class AppSchedulerBack(ABC):
    
    @abstractmethod
    def saveCreatedTime(self, method, run_date, job_id) -> None:
        pass