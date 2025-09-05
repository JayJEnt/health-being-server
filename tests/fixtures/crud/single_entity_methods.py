import pytest

from api.crud.single_entity import get_methods, post_methods, delete_methods, put_methods, search_methods


@pytest.fixture
def mocked_find_elements_by_name(mocked_supabase_connection_init, monkeypatch):
    monkeypatch.setattr(get_methods, "supabase_connection", mocked_supabase_connection_init)