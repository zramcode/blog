from celery import Celery
from config import settings
from email.message import EmailMessage
from fastapi import  HTTPException
import aiosmtplib , asyncio, traceback

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_BROKER_URL,  
)

@celery_app.task
def send_welcome_email(subject: str, recipient: str, body: str):
    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    async def send_email():
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            start_tls=True,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASS,
        )

    try:
        asyncio.run(send_email())
        return f"Email sent to {recipient}"
    except Exception as e:
        return f"Failed to send email: {e}"









 