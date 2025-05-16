from celery import Celery
from configs.config import settings
import aiosmtplib
from email.message import EmailMessage
import traceback
from fastapi import  HTTPException

celery_app = Celery(
    "tasks",
    broker=settings.redis_broker_url, 
    backend=settings.redis_broker_url
)
try:
 @celery_app.task
 def send_welcome_email(subject: str, recipient: str, body: str):
   message = EmailMessage()
   message["From"] = settings.SMTP_USER
   message["To"] = recipient
   message["Subject"] = subject
   message.set_content(body)
   try:
      aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            start_tls=True,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASS,
        )
      return(f"Email sent to {recipient}")
   except Exception as e:
        return(f"Failed to send email: {e}")
   
except Exception as e:
    traceback.print_exc()
    raise HTTPException(status_code=500, detail=str(e))
