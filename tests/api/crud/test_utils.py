import pytest

from api.crud.utils import pydantic_to_dict, get_main_config, get_relation_config


def test_pydantic_to_dict(example_pydantic_model, example_dict_response):
    result = pydantic_to_dict(example_pydantic_model)

    assert result == example_dict_response


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
        str(excinfo.value) == "Relation 'fake_input' not defined for element 'recipes'"
    )
