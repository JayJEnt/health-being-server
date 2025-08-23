"""Util functions operating on pydantic models and their attributes"""
from logger import logger
from api.crud.entity_mapping import ENTITY_MAPPING


def pop_attributes(pydantic_model, attributes):
    """Function for poping attributes from pydantic_model
    args:   pydantic_model [pydantic]
            attributes [list[str]]
    return: pydantic_model, poped_attributes
    """
    pydantic_model = pydantic_to_dict(pydantic_model)
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
    pydantic_model = pydantic_to_dict(pydantic_model)
    for attribute in attributes:
        logger.debug(f"Attribute about to add: {attribute}")
        for key, value in attribute.items():
            pydantic_model[key] = value
        logger.debug(f"Pydantic_model after new attribute: {pydantic_model}")

    return pydantic_model


def restrict_data(element_type: str, elements: list):
    """Function that filter data and drop restriction keys."""
    config = ENTITY_MAPPING[element_type]

    filtered_response = []
    for element in elements:
        filtered_element, popped_attributes = pop_attributes(
            element,
            [name for name in config["restricted"]]
        )
        filtered_response.append(filtered_element)

    return filtered_response


def pydantic_to_dict(pydantic_model):
    if not isinstance(pydantic_model, dict):
        try:
            pydantic_model = pydantic_model.model_dump()
        except:
            logger.error(f"Invalid input: {pydantic_model}")
            raise TypeError
    return pydantic_model


def get_main_config(element_type: str):
    """Get a config for main entity table"""
    config = ENTITY_MAPPING.get(element_type, None)

    if not config:
        raise ValueError(f"Table '{config}' not defined")
    
    return config


def get_relation_config(element_type: str, relation_name: str):
    """Get a config for relation/join table"""
    config = get_main_config(element_type)

    relation_config = next(
        (rel for rel in config["relation"] if rel["name"] == relation_name),
        None
    )
    if not relation_config:
        raise ValueError(f"Relation '{relation_name}' not defined for element '{element_type}'")
    
    return relation_config


def get_related_config(element_type: str, relation_name: str):
    """Get a config for related entity table"""
    relation_config = get_relation_config(element_type, relation_name)

    related_config = ENTITY_MAPPING.get(relation_config['name'], None)

    if not related_config:
        logger.error(f"Related '{relation_name}' config not defined in ENTITY_MAPPING")
        raise ValueError
    
    return relation_config