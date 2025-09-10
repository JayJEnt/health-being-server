import pytest
import pytest_asyncio

from api.crud.single_entity.post_methods import create_element


@pytest.fixture()
def example_users_data_create():
    return [
        {
            "user_id": 1,
            "height": "180",
            "weight": "75",
            "age": 25,
            "activity_level": "moderate",
            "silhouette": "mesomorph",
        },
        {
            "user_id": 2,
            "height": "165",
            "weight": "68",
            "age": 30,
            "activity_level": "active",
            "silhouette": "mesomorph",
        },
        {
            "user_id": 3,
            "height": "135",
            "weight": "48",
            "age": 10,
            "activity_level": "active",
            "silhouette": "mesomorph",
        },
    ]


@pytest_asyncio.fixture
async def example_users_data_injection(
    mock_supabase_connection, example_users_data_create
):
    for user_data in example_users_data_create:
        await create_element("user_data", user_data)


@pytest.fixture()
def example_users_data_response(example_users_data_create):
    return example_users_data_create


@pytest.fixture()
def example_users_data_update():
    return [
        {
            "user_id": 1,
            "height": "166.0",
            "weight": "63.0",
            "age": 27,
            "activity_level": "moderate",
            "silhouette": "mesomorph",
        },
        {
            "user_id": 2,
            "height": "175.0",
            "weight": "71.0",
            "age": 29,
            "activity_level": "active",
            "silhouette": "mesomorph",
        },
        {
            "user_id": 3,
            "height": "165",
            "weight": "58",
            "age": 13,
            "activity_level": "active",
            "silhouette": "mesomorph",
        },
    ]


@pytest.fixture()
def example_users_data_update_response(example_users_data_update):
    return example_users_data_update
