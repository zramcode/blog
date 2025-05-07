from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import os

load_dotenv() 

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    smtp_host: str = Field(alias="SMTP_HOST")
    smtp_port: int = Field(alias="SMTP_PORT")
    smtp_user: str = Field(alias="SMTP_USER")
    smtp_pass: str = Field(alias="SMTP_PASS")

    # Redis broker for Celery
    redis_broker_url: str = Field(alias="REDIS_BROKER_URL")
    class Config:
        env_file = ".env"


settings = Settings()