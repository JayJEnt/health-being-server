from database.supabase_connection import supabase_connection
from config import settings


def get_user_by_email(email: str):
    user = supabase_connection.find_by(
        settings.USER_TABLE,
        "email",
        email,
    )
    return user[0]