from abc import ABC, abstractmethod


class MailSendingAPI(ABC):
    @abstractmethod
    def send_verification_email(self, to: str) -> str | None:
        pass