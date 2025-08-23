from logger import logger
from database.supabase_connection import supabase_connection
from api.handlers.exceptions import ResourceNotFound
from api.crud.utils import get_relation_config


async def get_relationships(
    element_type: str,
    relation_name: str,
    relation_id: int
) -> list:
    """
    Get relationships between an element and one related item by relation item id's.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        relation_name (str): The name of the relation (e.g., "ingredients").
        relation_id (int): The ID of the relation element.

    Returns:
        list: List of relationship items data.
    """
    relation_config = get_relation_config(element_type, relation_name)
    
    try:
        element = supabase_connection.find_by(
            relation_config["join_table"],
            relation_config["join_keys"][1],
            relation_id,
        )
    except ResourceNotFound:
        logger.info(f"No {relation_config['name']} entries found for {relation_config['join_keys'][1]}={relation_id}")
        raise

    return element


async def get_relationship(
    element_type: str,
    element_id: int,
    relation_name: str,
    relation_id: int
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
        element = supabase_connection.find_join_record(
            relation_config["join_table"],
            relation_config["join_keys"][0],
            element_id,
            relation_config["join_keys"][1],
            relation_id,
        )
    except ResourceNotFound:
        logger.info(f"No {relation_config['name']} entries found for {relation_config['join_keys'][1]}={relation_id}")
        raise

    return element