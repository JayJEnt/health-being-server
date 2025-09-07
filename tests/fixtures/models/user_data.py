import pytest
import pytest_asyncio


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
    ]


@pytest_asyncio.fixture
async def example_users_data_injection(
    mock_supabase_connection, example_users_data_create
):
    from api.crud.single_entity.post_methods import create_element

    for user_data in example_users_data_create:
        await create_element("user_data", user_data)


@pytest.fixture()
def example_users_data_response(example_users_data_create):
    return example_users_data_create
