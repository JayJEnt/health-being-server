import pytest

from api.schemas.vitamin import VitaminCreate
from api.crud.utils import pydantic_to_dict, get_main_config, get_relation_config


vitamin_dict = {"name": "C12"}

vitamin_pydantic = VitaminCreate(**vitamin_dict)


def test_pydantic_to_dict():
    result = pydantic_to_dict(vitamin_pydantic)

    assert result == vitamin_dict


def test_pydantic_to_dict_error():
    with pytest.raises(Exception) as excinfo:
        pydantic_to_dict("fake_input")

    assert str(excinfo.value) == "'str' object has no attribute 'model_dump'"


def test_get_main_config_error():
    with pytest.raises(Exception) as excinfo:
        get_main_config("fake_input")

    assert str(excinfo.value) == "Table 'fake_input' not defined"


def test_get_relation_config_error():
    with pytest.raises(Exception) as excinfo:
        get_relation_config("recipes", "fake_input")

    assert (
        str(excinfo.value)
        == "Relation 'fake_input' type 'relation' not defined for element 'recipes'"
    )
