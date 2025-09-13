import pytest
import pytest_asyncio

from api.crud.single_entity.post_methods import create_element


@pytest.fixture()
def example_users_data_create():
    return [
        {
            "user_id": 1,
            "height": "180.0",
            "weight": "75.0",
            "age": 25,
            "activity_level": "moderate",
            "silhouette": "ectomorph",
        },
        {
            "user_id": 2,
            "height": "165.0",
            "weight": "68.0",
            "age": 30,
            "activity_level": "very",
            "silhouette": "mesomorph",
        },
        {
            "user_id": 3,
            "height": "135.0",
            "weight": "48.0",
            "age": 10,
            "activity_level": "light",
            "silhouette": "endomorph",
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
    return [
        {
            "user_id": 1,
            "height": 180.0,
            "weight": 75.0,
            "age": 25,
            "activity_level": "moderate",
            "silhouette": "ectomorph",
        },
        {
            "user_id": 2,
            "height": 165.0,
            "weight": 68.0,
            "age": 30,
            "activity_level": "very",
            "silhouette": "mesomorph",
        },
        {
            "user_id": 3,
            "height": 135.0,
            "weight": 48.0,
            "age": 10,
            "activity_level": "light",
            "silhouette": "endomorph",
        },
    ]


@pytest.fixture()
def example_users_data_update():
    return [
        {
            "user_id": 1,
            "height": "166.0",
            "weight": "63.0",
            "age": 27,
            "activity_level": "moderate",
            "silhouette": "ectomorph",
        },
        {
            "user_id": 2,
            "height": "175.0",
            "weight": "71.0",
            "age": 29,
            "activity_level": "very",
            "silhouette": "mesomorph",
        },
        {
            "user_id": 3,
            "height": "165.0",
            "weight": "58.0",
            "age": 13,
            "activity_level": "light",
            "silhouette": "endomorph",
        },
    ]


@pytest.fixture()
def example_users_data_update_response():
    return [
        {
            "user_id": 1,
            "height": 166.0,
            "weight": 63.0,
            "age": 27,
            "activity_level": "moderate",
            "silhouette": "ectomorph",
        },
        {
            "user_id": 2,
            "height": 175.0,
            "weight": 71.0,
            "age": 29,
            "activity_level": "very",
            "silhouette": "mesomorph",
        },
        {
            "user_id": 3,
            "height": 165.0,
            "weight": 58.0,
            "age": 13,
            "activity_level": "light",
            "silhouette": "endomorph",
        },
    ]
