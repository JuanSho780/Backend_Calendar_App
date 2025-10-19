from app.domain.apis.mail_sending_api import MailSendingAPI
from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random

class MailSendingAPIImpl(MailSendingAPI):
    def send_verification_email(self, to: str) -> str | None:
        load_dotenv()

        random_verification_code = str(random.randint(100000, 999999))

        message = Mail(
            from_email=os.getenv("SENDGRID_FROM_EMAIL"),
            to_emails=to,
            subject="Please verify your email (PlinifyMe)",
            html_content=f"<strong>This is your verification code: {random_verification_code}</strong>"
        )

        try:
            sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
            # sg.set_sendgrid_data_residency("eu")
            # uncomment the above line if you are sending mail using a regional EU subuser
            response = sg.send(message)
            print(response.status_code)
            return random_verification_code
        
        except Exception as e:
            print(e)
            return None