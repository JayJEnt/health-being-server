from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.utils import get_main_config, pydantic_to_dict


async def create_element(element_type: str, element_data: dict) -> dict:
    """
    Create a record in element table.

    Args:
        element_type (str): The type of the element (e.g., "recipes").
        element_data (dict): The element item data
        (e.g., {"username": "test_user", "email": "test_user@example.com", "password": "123"}).

    Returns:
        dict: Element item response data from database.
    """
    config = get_main_config(element_type)
    element_data = pydantic_to_dict(element_data)

    element_data = supabase_connection.insert(
        config["table"],
        element_data
    )
    logger.debug(f"Element: {element_data} inserted to table {config['table']}.")

    return element_data