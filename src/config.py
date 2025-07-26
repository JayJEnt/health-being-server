from pydantic_settings import BaseSettings
from dotenv import load_dotenv

import os


class LocalSettings(BaseSettings):
    environment: str = "local"
    log_level: str = "DEBUG"
    
    # AWS
    aws_region: str = "eu-north-1"

    # SUPABASE SECRETS
    supabase_url: str = ""
    supabase_key: str = ""

    # TABLES
    recipe_table: str = ""
    user_table: str = ""
    ingredient_table: str = ""
    diet_type_table: str = ""
    diet_type_included_table: str =""

    load_dotenv()
    
class Settings(BaseSettings):
    environment: str = os.getenv("environment", "remote")
    log_level: str = "INFO"
    
    # AWS
    aws_region: str = "eu-north-1"

    # SUPABASE SECRETS
    supabase_url: str = ""
    supabase_key: str = ""

    # TABLES
    recipe_table: str = ""
    user_table: str = ""
    ingredient_table: str = ""
    diet_type_table: str = ""
    diet_type_included_table: str =""

    load_dotenv()

settings = Settings() if os.getenv("environment", "").lower() == "remote" else LocalSettings()