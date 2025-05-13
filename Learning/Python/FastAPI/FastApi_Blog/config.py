from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SMTP_HOST: str 
    SMTP_PORT: int 
    SMTP_USER: str 
    SMTP_PASS: str 

    REDIS_BROKER_URL: str 

    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()