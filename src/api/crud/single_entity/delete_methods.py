from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.utils import get_main_config
from api.handlers.exceptions import ResourceNotFound


async def delete_element_by_id(element_type: str, element_id: int) -> dict:
    """
    Delete a record in element table by it's id

    Args:
        element_type (str): The type of the element (e.g., "recipes").
        element_id (int): The ID of the element.

    Returns:
        dict: Element item response data from database.
    """
    config = get_main_config(element_type)

    try:
        element = supabase_connection.delete_by(
            config["table"],
            config["id"],
            element_id
        )
    except ResourceNotFound:
        logger.error(f"{element_type} with id={element_id} not found in database")
        raise

    return element