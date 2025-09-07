import pytest

from api.schemas.vitamin import VitaminCreate


vitamin_dict = {"name": "C12"}


@pytest.fixture
def example_pydantic_model():
    return VitaminCreate(**vitamin_dict)


@pytest.fixture
def example_dict_response():
    return vitamin_dict
