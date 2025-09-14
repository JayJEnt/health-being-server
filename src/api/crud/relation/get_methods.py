import asyncio

from api.crud.utils import get_relation_config, get_related_config
from api.handlers.exceptions import ResourceNotFound
from database.supabase_connection import supabase_connection
from logger import logger


async def get_relationship(
    element_type: str, element_id: int, relation_name: str, relation_id: int
) -> dict:
    """
    Get single relationship between an element and one related item by their's id

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relation_name (str): The name of the relation (e.g., "ingredients").
        relation_id (int): The ID of the relation element.

    Returns:
        dict: Relationship item data.
    """
    relation_config = get_relation_config(element_type, relation_name)

    try:
        element = await supabase_connection.find_join_record(
            relation_config["join_table"],
            relation_config["join_keys"][0],
            element_id,
            relation_config["join_keys"][1],
            relation_id,
        )
    except ResourceNotFound:
        logger.info(
            f"No {relation_config['name']} entries found for {relation_config['join_keys'][0]}={element_id}"
        )
        raise

    return element


async def get_relationships(
    element_type: str,
    element_id: int,
    relation_name: str,
) -> list:
    """
    Get relationships between an element and one related item by relation item id's.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relations (list): The list of all elements that are related to the element table. (e.g., ["ingredients", "diet_type"])

    Returns:
        list: List of relationship items data.
    """
    relation_config = get_relation_config(element_type, relation_name)
    try:
        element = await supabase_connection.find_by(
            relation_config["join_table"],
            relation_config["join_keys"][0],
            element_id,
        )
    except ResourceNotFound:
        logger.info(
            f"No {relation_config['name']} entries found for {relation_config['join_keys'][0]}={element_id}"
        )
        raise

    return element


async def get_relationed_item(
    element_type: str,
    element_id: int,
    relation_name: str,
):
    """
    Get data from relationship table (N:M) to get element with it's relation attributes.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relation_name (str): The type of the relation element (e.g., "ingredients").

    Returns:
        list: List of attributes from foreign tables
    """
    relation_config = get_relation_config(element_type, relation_name)
    try:
        element = await supabase_connection.find_by(
            relation_config["join_table"],
            relation_config["join_keys"][0],
            element_id,
        )
    except ResourceNotFound:
        logger.info(
            f"No {relation_config['name']} entries found for "
            f"{relation_config['join_keys'][0]}={element_id}"
        )
        raise

    logger.debug(element)
    related_items = await asyncio.gather(*(get_item(element_type, relation_name, item) for item in element))
    return {relation_config["name"]: related_items}


async def get_item(element_type: str, relation_name: str, item: list):
    """
    Get a item 'extra_fields' from foreign table

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        relation_name (str): The type of the relation element (e.g., "ingredients").
        item (list): The list of element attributes retrived from join table

    Returns:
        list: List of items of 1 foreign table
    """
    related_config = get_related_config(element_type, relation_name)
    relation_config = get_relation_config(element_type, relation_name)

    try:
        related_item = await supabase_connection.find_by(
            related_config["table"],
            related_config["id"],
            item[relation_config["join_keys"][1]],
        )
    except ResourceNotFound:
        logger.error(
            f"Couldn't find item: {relation_config['name']} in {related_config['table']}. "
            "The previously found relationship is matching a non-existing item!"
        )
        raise

    related_item_data = dict(related_item[0])

    for field in relation_config.get("extra_fields", []):
        related_item_data[field] = item[field]

    return related_item_data
