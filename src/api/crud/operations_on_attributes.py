"""Util functions operating on pydantic models and their attributes"""
from logger import logger


def pop_attributes(pydantic_model, attributes):
    """Function for poping attributes from pydantic_model
    args:   pydantic_model [pydantic]
            attributes [list[str]]
    return: pydantic_model, poped_attributes
    """
    if not isinstance(pydantic_model, dict):
        try:
            pydantic_model = pydantic_model.model_dump()
        except:
            logger.error(f"Invalid input: {pydantic_model}")
            raise TypeError
    poped_attributes = []

    for attribute in attributes:
        poped_attribut = pydantic_model.get(f"{attribute}", "")
        logger.debug(f"Poped_attribut: {poped_attribut}")
        poped_attributes.append(poped_attribut)

        pydantic_model = {key : value for key, value in pydantic_model.items() if key != f"{attribute}"}
        logger.debug(f"Pydantic_model after drop of attribut: {pydantic_model}")

    return pydantic_model, poped_attributes

def add_attributes(pydantic_model, attributes):
    """Function for adding attributes to pydantic_model
    args:   pydantic_model [json]
            attributes [list[dict]]
    return: pydantic_model
    """
    if not isinstance(pydantic_model, dict):
        try:
            pydantic_model = pydantic_model.model_dump()
        except:
            logger.error(f"Invalid input: {pydantic_model}")
            raise TypeError
    for attribute in attributes:
        logger.debug(f"Attribute about to add: {attribute}")
        for key, value in attribute.items():
            pydantic_model[key] = value
        logger.debug(f"Pydantic_model after new attribute: {pydantic_model}")

    return pydantic_model