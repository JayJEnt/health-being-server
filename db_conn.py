from supabase import create_client, Client
from typing import Any

from config import settings

class SupabaseConnection:
    def __init__(self):
        self._url = settings.supabase_url
        self._key = settings.supabase_key
        self._client: Client = create_client(self._url, self._key)

    def fetch_all(self, table: str) -> list[dict[str, Any]]:
        response = self._client.table(table).select("*").execute()
        if response.error:
            raise Exception(f"Select Error: {response.error.message}")
        return response.data

    def insert(self, table: str, data: dict) -> list[dict[str, Any]]:
        response = self._client.table(table).insert(data).execute()
        if response.error:
            raise Exception(f"Insert Error: {response.error.message}")
        return response.data

    def find_by(self, table: str, column: str, value: Any) -> list[dict[str, Any]]:
        response = self._client.table(table).select("*").eq(column, value).execute()
        if response.error:
            raise Exception(f"Query Error: {response.error.message}")
        return response.data

    def delete_by(self, table: str, column: str, value: Any) -> list[dict[str, Any]]:
        response = self._client.table(table).delete().eq(column, value).execute()
        if response.error:
            raise Exception(f"Delete Error: {response.error.message}")
        return response.data

    def update_by(self, table: str, column: str, value: Any, updates: dict) -> list[dict[str, Any]]:
        response = self._client.table(table).update(updates).eq(column, value).execute()
        if response.error:
            raise Exception(f"Update Error: {response.error.message}")
        return response.data
