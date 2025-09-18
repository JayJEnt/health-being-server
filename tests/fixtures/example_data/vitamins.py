import pytest
import pytest_asyncio

from api.crud.single_entity.post_methods import create_element


@pytest.fixture()
def example_vitamins_create():
    return [
        {"name": "C"},
        {"name": "D"},
    ]


@pytest_asyncio.fixture
async def example_vitamins_injection(mock_supabase_connection, example_vitamins_create):
    for vitamin in example_vitamins_create:
        await create_element("vitamins", vitamin)


@pytest.fixture()
def example_vitamins_response():
    return [
        {"id": 1, "name": "C"},
        {"id": 2, "name": "D"},
    ]


@pytest.fixture()
def example_vitamins_update():
    return [
        {"name": "C12"},
        {"name": "D6"},
    ]


@pytest.fixture()
def example_vitamins_update_response():
    return [
        {"id": 1, "name": "C12"},
        {"id": 2, "name": "D6"},
    ]
