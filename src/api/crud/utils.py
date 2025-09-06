"""Util functions for CRUD operations"""

from logger import logger
from api.crud.entity_mapping import ENTITY_MAPPING


# TODO: FIX DOCS maybe
def pop_attributes(pydantic_model, attributes):
    """
    Pop attributes from pydantic_model

    Args:
        pydantic_model [pydantic]
        attributes [list[str]]

    Return:
        pydantic_model [json], poped_attributes [list[dict]]
    """
    logger.debug(f"Pydantic model before pop operation: {pydantic_model}")
    pydantic_model = pydantic_to_dict(pydantic_model)
    poped_attributes = []
    for attribute in attributes:
        poped_attribut = pydantic_model.get(f"{attribute}", "")
        poped_attribut = {attribute: poped_attribut}
        logger.debug(f"Poped attribut: {poped_attribut}")
        poped_attributes.append(poped_attribut)

        pydantic_model = {
            key: value for key, value in pydantic_model.items() if key != f"{attribute}"
        }
        logger.debug(f"Pydantic model after drop of attribut: {pydantic_model}")

    return pydantic_model, poped_attributes


def add_attributes(pydantic_model, attributes):
    """
    Add attributes to pydantic_model

    Args:
        pydantic_model [json]
        attributes [list[dict]]

    Return:
        pydantic_model [pydantic]
    """
    logger.debug(f"Pydantic model before add operation: {pydantic_model}")
    pydantic_model = pydantic_to_dict(pydantic_model)
    for attribute in attributes:
        logger.debug(f"Attribute to add: {attribute}")
        for key, value in attribute.items():
            pydantic_model[key] = value
        logger.debug(f"Pydantic model after new attribute: {pydantic_model}")

    return pydantic_model


def restrict_data(element_type: str, elements: list):
    """Function that filter data and drop restriction keys."""
    config = ENTITY_MAPPING[element_type]

    filtered_response = []
    for element in elements:
        filtered_element, popped_attributes = pop_attributes(
            element, [restricted for restricted in config["restricted"]]
        )
        filtered_response.append(filtered_element)

    return filtered_response


def pydantic_to_dict(pydantic_model):
    """Transform pydantic model into dictionary."""
    if not isinstance(pydantic_model, dict):
        try:
            pydantic_model = pydantic_model.model_dump()
        except TypeError:
            logger.error(f"Invalid input: {pydantic_model}")
            raise
    return pydantic_model


def get_main_config(element_type: str):
    """Get a config for main entity table"""
    config = ENTITY_MAPPING.get(element_type, None)

    if not config:
        raise ValueError(f"Table '{element_type}' not defined")

    return config


def get_relation_config(
    element_type: str, relation_name: str, relation_type: str = "relation"
):
    """
    Get a config for relation/join table

    Args:
        relation_type (str): Optional parameter switches between [relation/nested]
    """
    config = get_main_config(element_type)

    relation_config = next(
        (
            relation
            for relation in config[relation_type]
            if relation["name"] == relation_name
        ),
        None,
    )
    if not relation_config:
        raise ValueError(
            f"Relation '{relation_name}' type '{relation_type}' not defined for element '{element_type}'"
        )

    return relation_config


def get_related_config(
    element_type: str, relation_name: str, relation_type: str = "relation"
):
    """Get a config for related entity table"""
    relation_config = get_relation_config(element_type, relation_name, relation_type)

    related_config = ENTITY_MAPPING.get(relation_config["name"], None)

    if not related_config:
        logger.error(f"Related '{relation_name}' config not defined in ENTITY_MAPPING")
        raise ValueError

    return related_config
