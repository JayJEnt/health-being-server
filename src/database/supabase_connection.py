from supabase import create_client, Client

from typing import Any, Dict, Optional
from functools import wraps

from api.handlers.exceptions import RescourceNotFound, InternalServerError
from config import settings
from logger import logger


class SupabaseConnection:
    def __init__(self):
        self._url = settings.supabase_url
        self._key = settings.supabase_key
        try:
            self._client: Client = create_client(self._url, self._key)
        except Exception as ex:
            logger.error(f"Supabase connection error: {ex}")
            raise ConnectionRefusedError

    @staticmethod
    def error_handler(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.info(f"Processing request: {func.__name__}")
                result = func(*args, **kwargs)
                if result is None:
                    func_args = args[1:] if args and args[0].__class__.__name__ == "SupabaseConnection" else args
                    logger.info(
                        f"Resource not found - Operation: {func.__name__}, "
                        f"Args: {func_args}"
                    )
                    raise RescourceNotFound
                logger.info(f"Sucesfully processed.")
                return result
            except RescourceNotFound:
                raise RescourceNotFound
            except Exception as ex:
                logger.error(f"Supabase error: {ex}")
                raise InternalServerError
        return wrapper

    @error_handler
    def fetch_all(self, table: str) -> Optional[list[Dict[str, Any]]]:
        response = (
            self._client.table(table)
            .select("*")
            .execute()
        )
        if not response.data:
            return None
        return response.data

    @error_handler
    def insert(self, table: str, data: dict) -> Optional[Dict[str, Any]]:
        response = (
            self._client.table(table)
            .insert(data)
            .execute()
        )
        if not response.data:
            return None
        return response.data[0]

    @error_handler
    def find_by(self, table: str, column: str, value: Any) -> Optional[list[Dict[str, Any]]]:
        response = (
            self._client.table(table)
            .select("*")
            .eq(column, value)
            .execute()
        )
        if not response.data:
            return None
        return response.data

    @error_handler
    def delete_by(self, table: str, column: str, value: Any) -> Optional[Dict[str, Any]]:
        response = (
            self._client.table(table)
            .delete()
            .eq(column, value)
            .execute()
        )
        if not response.data:
            return None
        return response.data[0]

    @error_handler
    def update_by(self, table: str, column: str, value: Any, updates: dict) -> Optional[Dict[str, Any]]:
        response = (
            self._client.table(table)
            .update(updates)
            .eq(column, value)
            .execute()
        )
        if not response.data:
            return None
        return response.data[0]

supabase_connection = SupabaseConnection()