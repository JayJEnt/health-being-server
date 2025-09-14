from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.utils import get_relation_config
from api.handlers.exceptions import ResourceNotFound


async def delete_relationship(
    element_type: str, element_id: int, relation_name: str, relation_id: int
) -> dict:
    """
    Delete relationship between an element and one related item.

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
        element = await supabase_connection.delete_join_record(
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


async def delete_relationships(
    element_type: str,
    element_id: int,
    relations: list,
) -> dict:
    """
    Delete relationships of the relation item id's.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relations (list): The list of all elements that are related to the element table. (e.g., ["ingredients", "diet_type"])

    Returns:
        dict: Relationship item data.
    """
    for relation_name in relations:
        relation_config = get_relation_config(element_type, relation_name)
        try:
            await supabase_connection.delete_by(
                relation_config["join_table"],
                relation_config["join_keys"][0],
                element_id,
            )
        except ResourceNotFound:
            logger.info(
                f"No {relation_config['name']} entries found for {relation_config['join_keys'][0]}={element_id}"
            )
