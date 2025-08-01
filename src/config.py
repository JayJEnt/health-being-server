from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from typing import Optional
import os


class Settings(BaseSettings):
    # AWS
    aws_region: str = "eu-north-1"
    
    # SUPABASE SECRETS
    supabase_url: str = ""
    supabase_key: str = ""

    # TABLES
    recipe_table: str = ""
    recipe_favourite: str = ""
    user_table: str = ""
    user_data_table: str = ""
    follow_table: str = ""
    prefered_ingredients_table: str = ""
    prefered_recipe_type_table: str = ""
    refrigerator_table: str = ""
    ingredient_table: str = ""
    ingredients_included_table: str = ""
    diet_type_table: str = ""
    diet_type_included_table: str = ""
    vitamin_table: str = ""
    vitamins_included_table: str = ""

    # AUTHENTICATION
    secret_key: str = ""
    algorithm: str = ""
    access_token_expire: Optional[int] = None

    load_dotenv()

class LocalSettings(Settings):
    environment: str = "local"
    log_level: str = "DEBUG"
    
class RemoteSettings(Settings):
    environment: str = os.getenv("environment", "remote")
    log_level: str = "INFO"

settings = RemoteSettings() if os.getenv("environment", "").lower() == "remote" else LocalSettings()