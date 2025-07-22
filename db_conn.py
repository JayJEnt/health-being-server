from supabase import create_client, Client

from typing import Any
from functools import wraps

from config import settings
from logger import configure_logger


class SupabaseConnection:
    def __init__(self):
        self._url = settings.supabase_url
        self._key = settings.supabase_key
        self._client: Client = create_client(self._url, self._key)

    @staticmethod
    def error_handler(func):
        logger = configure_logger()

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                logger.error(f"Supabase error: {ex}")
                return None
        return wrapper

    @error_handler
    def fetch_all(self, table: str) -> list[dict[str, Any]]:
        response = (
            self._client.table(table)
            .select("*")
            .execute()
        )
        return response.data

    @error_handler
    def insert(self, table: str, data: dict) -> list[dict[str, Any]]:
        response = (
            self._client.table(table)
            .insert(data)
            .execute()
        )
        return response.data

    @error_handler
    def find_by(self, table: str, column: str, value: Any) -> list[dict[str, Any]]:
        response = (
            self._client.table(table)
            .select("*")
            .eq(column, value)
            .execute()
        )
        return response.data

    @error_handler
    def delete_by(self, table: str, column: str, value: Any) -> list[dict[str, Any]]:
        response = (
            self._client.table(table)
            .delete()
            .eq(column, value)
            .execute()
        )
        return response.data

    @error_handler
    def update_by(self, table: str, column: str, value: Any, updates: dict) -> list[dict[str, Any]]:
        response = (
            self._client.table(table)
            .update(updates)
            .eq(column, value)
            .execute()
        )
        return response.data
