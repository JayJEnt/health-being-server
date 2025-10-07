from api.crud.relation.get_methods import get_relationships_and_related_tables
from api.crud.utils import add_attributes, get_main_config
from api.handlers.http_exceptions import ResourceNotFound
from database.supabase_connection import supabase_connection
from logger import logger


async def get_all(
    element_type: str,
    element_id: int,
    related_attributes: list = [],
) -> dict:
    """
    Get all (entity, relationships) data for an element by its id and specified related attributes.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        related_attributes (list, optional): List of related attributes to include. Defaults to [].

    Returns:
        dict: Relationship item data.
    """
    config = get_main_config(element_type)

    try:
        element_data = supabase_connection.find_by(
            config["table"],
            config["id"],
            element_id,
        )[0]
    except ResourceNotFound:
        logger.error(f"{element_type} with id={element_id} not found")
        raise

    attributes_to_add = await get_relationships_and_related_tables(
        element_type, element_id, related_attributes
    )

    element_data = add_attributes(element_data, attributes_to_add)

    return element_data
