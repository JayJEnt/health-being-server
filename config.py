import os
from pydantic_settings import BaseSettings


class LocalSettings(BaseSettings):
    environment: str = "local"
    log_level: str = "DEBUG"
    
    # AWS
    aws_region: str = "eu-north-1"
    
class Settings(BaseSettings):
    environment: str = os.getenv("environment", "remote")
    log_level: str = "INFO"
    
    # AWS
    aws_region: str = "eu-north-1"

if os.environ.get("environment", "") == "remote":
    settings = Settings()
else:
    settings = LocalSettings()