from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.single_entity.get_methods import get_element_by_name
from api.crud.utils import pydantic_to_dict, get_relation_config, get_related_config
from api.handlers.exceptions import ResourceNotFound, ReferencesToItself


async def create_relationship(
    element_type: str,
    element_id: int,
    relation_name: str,
    related_data: dict
) -> dict:
    """
    Create a single relationship between an element and one related item.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relation_name (str): The name of the relation (e.g., "ingredients").
        related_data (dict): Data for the related element, including identifying column and optional extra fields.

    Returns:
        dict: Related item data (with extra fields if any).
    """
    related_data = pydantic_to_dict(related_data)
    if element_type == relation_name and element_id == related_data["id"]:
        logger.error(f"Element {element_type} with id={element_id} tries to reference to itself.")
        raise ReferencesToItself

    relation_config = get_relation_config(element_type, relation_name)
    related_config = get_related_config(element_type, relation_name)

    try:
        exists = await get_element_by_name(relation_config['name'], related_data[related_config['column_name']])
    except ResourceNotFound:
        logger.error(f"{relation_config['name']} '{related_data[related_config['column_name']]}' not recognized")
        return None

    related_item = {**exists}
    join_data = {
        relation_config["join_keys"][0]: element_id,
        relation_config["join_keys"][1]: exists["id"]
    }
    if "extra_fields" in relation_config:
        for field in relation_config["extra_fields"]:
            if field in related_data:
                related_item[field] = related_data[field]
                join_data[field] = related_data[field]

    supabase_connection.insert(relation_config["join_table"], join_data)
    logger.debug(f"Relation element: {join_data} inserted to table {relation_config['join_table']}.")

    return related_item


async def create_relationships(
    element_type: str,
    element_id: int,
    related_data: list,
) -> list:
    """
    Create relationships between an element and one related items.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        related_data (list): The list of all lists of all elements that are related to the element table.
        (e.g., ["ingredients": ["marchewka", "pomidor"], "diet_type": ["vege", "vegan"]])

    Returns:
        list[dict]: List of related items data (with extra fields if any).
    """
    attributes_to_add = []
    for related_element_list in related_data:
        related_items = []

        relation_name, related_data = next(iter(related_element_list.items()))
        relation_config = get_relation_config(element_type, relation_name)

        for item in related_data:
            related_item = await create_relationship(element_type, element_id, relation_name, item)
            related_items.append(related_item)

        attributes_to_add.append({relation_config["name"]: related_items})

    return attributes_to_add