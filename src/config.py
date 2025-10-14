from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional, List
import os


class Settings(BaseSettings):
    """AWS"""

    # AWS S3 BUCKET
    AWS_REGION: str = "eu-north-1"
    BUCKET_NAME: str = "health-being-server-api"

    """DATABASE"""
    # SUPABASE SECRETS
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # TEST DATABASE
    TEST_DATABASE_URL: str = "sqlite:///:memory:"

    # TABLES
    RECIPE_TABLE: str = "recipes"
    RECIPE_FAVOURITE: str = "recipe_favourite"
    USER_TABLE: str = "users"
    FOLLOW_TABLE: str = "follows"
    PREFERED_INGREDIENTS_TABLE: str = "prefered_ingredients"
    PREFERED_RECIPE_TYPE_TABLE: str = "prefered_recipe_type"
    REFRIGERATOR_TABLE: str = "refrigerator"
    INGREDIENT_TABLE: str = "ingredients"
    INGREDIENTS_INCLUDED_TABLE: str = "ingredients_included"
    DIET_TYPE_TABLE: str = "diet_types"
    DIET_TYPE_INCLUDED_TABLE: str = "diet_type_included"
    VITAMIN_TABLE: str = "vitamins"
    VITAMINS_INCLUDED_TABLE: str = "vitamins_included"

    """AUTHENTICATION"""
    # OUR SECRETS
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE: Optional[int] = None

    # EXTERNAL PROVIDERS
    EXTERNAL_PROVIDERS: List[str] = ["google"]

    # GOOGLE SECRETS
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""
    GOOGLE_AUTH_ENDPOINT: str = ""
    GOOGLE_TOKEN_ENDPOINT: str = ""
    GOOGLE_USERINFO_ENDPOINT: str = ""

    # EMAIL SECRETS
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""

    # EMAIL CONFIG
    MAIL_FROM: str = "jivonaypm@gmail.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "health-being-app"
    MAIL_EXPIRE_TIME: int = 5
    MAIL_FRONTEND_CALLBACK: str = "http://127.0.0.1:8000/oauth2/verify_email"

    load_dotenv()


class LocalSettings(Settings):
    """ENVIORNMENT CONFIG"""

    ENVIRONMENT: str = "local"
    LOG_LEVEL: str = "DEBUG"


class RemoteSettings(Settings):
    """ENVIORNMENT CONFIG"""

    ENVIRONMENT: str = "remote"
    LOG_LEVEL: str = "INFO"


def get_settings() -> Settings:
    return (
        RemoteSettings()
        if os.getenv("ENVIRONMENT", "").lower() == "remote"
        else LocalSettings()
    )


settings = get_settings()
