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

        subject = "🔐 Please verify your email - PlanifyMe"

        html_content = f"""
        <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 30px; border: 1px solid #e0e0e0; border-radius: 10px; background-color: #ffffff;">
            
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="color: #333; margin: 0; font-size: 24px;">Welcome to PlanifyMe! 👋</h2>
                <p style="color: #666; font-size: 16px; margin-top: 10px;">Let's get you verified.</p>
            </div>

            <p style="color: #555; font-size: 16px; text-align: center; line-height: 1.5;">
                Use the following code to complete your registration process. 
                This code is valid for <strong>10 minutes</strong>.
            </p>

            <div style="background-color: #f0f7ff; border: 1px dashed #007bff; border-radius: 8px; padding: 20px; margin: 30px 0; text-align: center;">
                <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #2c3e50; font-family: monospace;">
                    {random_verification_code}
                </span>
            </div>

            <p style="color: #999; font-size: 14px; text-align: center; margin-bottom: 30px;">
                If you didn't request this code, you can safely ignore this email.
            </p>

            <div style="border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #888; font-size: 14px;">
                Your assistant,<br>
                <strong style="color: #007bff; font-size: 16px;">PlanifyMe</strong>
            </div>

        </div>
        """

        message = Mail(
            from_email=os.getenv("SENDGRID_FROM_EMAIL"),
            to_emails=to,
            subject=subject,
            html_content=html_content
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
        
    def send_notification_email(self, to: str, subject: str, content: str) -> bool:
        message = Mail(
            from_email=os.getenv("SENDGRID_FROM_EMAIL"),
            to_emails=to,
            subject=subject,
            html_content=content
        )

        try:
            sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
            response = sg.send(message)
            print(response.status_code)
            return True
            
        except Exception as e:
            print(e)
            return False