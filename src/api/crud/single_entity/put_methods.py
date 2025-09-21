from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.utils import get_main_config, pydantic_to_dict
from api.handlers.http_exceptions import ResourceNotFound


async def update_element_by_id(
    element_type: str, element_id: int, element_data: dict
) -> dict:
    """
    Update a record in element table by it's id.

    Args:
        element_type (str): The type of the element (e.g., "recipes").
        element_id (int): The ID of the element.
        element_data (dict): The element item data
        (e.g., {"username": "test_user", "email": "test_user@example.com", "hashed_password": "&9sjoahe)2sJ2laSJ!@"}).

    Returns:
        dict: Element item response data from database.
    """
    config = get_main_config(element_type)
    element_data = pydantic_to_dict(element_data)

    try:
        element_data = supabase_connection.update_by(
            config["table"],
            config["id"],
            element_id,
            element_data,
        )
        logger.debug(f"Element: {element_data} in table {config['table']} got updated.")
    except ResourceNotFound:
        logger.error(f"{element_type} with id={element_id} not found in database")
        raise

    return element_data
