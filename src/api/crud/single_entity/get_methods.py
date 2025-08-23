from database.supabase_connection import supabase_connection
from api.handlers.exceptions import ResourceNotFound
from api.crud.utils import restrict_data, get_main_config
from logger import logger


async def get_elements(element_type: str, restrict: bool=False) -> dict:
    """
    Get all records in element table.

    Args:
        element_type (str): The type of the element (e.g., "recipes").
        restrict (bool): The optional argument, that allows to drop some of the attributes.

    Returns:
        dict: Element item response data from database.
    """
    config = get_main_config(element_type)

    elements_response = supabase_connection.fetch_all(config["table"])
    if restrict:
        elements_response = restrict_data(element_type, elements_response)

    return elements_response


async def get_element_by_name(element_type: str, element_name: str, alternative_name: bool=False) -> dict:
    """
    Get a record in element table by element's name.

    Args:
        element_type (str): The type of the element (e.g., "recipes").
        element_name (str): The name of the element (e.g., "Marchewka").
        alternative_name (bool): The optional argument, that allows to search by diffrent column name.

    Returns:
        dict: Element item response data from database.
    """
    config = get_main_config(element_type)

    if alternative_name:
        column_name = config["alternative_column_name"]
    else:
        column_name = config["column_name"]

    elements = supabase_connection.find_ilike(
        config["table"],
        column_name,
        element_name,
    )
    if not elements or elements[0][column_name].lower()!=element_name.lower():
        logger.error(f"{element_type} with name={element_name} not found")
        raise ResourceNotFound
    return elements[0]


async def get_element_by_id(element_type: str, element_id: int) -> dict:
    """
    Get a record in element table by it's id.

    Args:
        element_type (str): The type of the element (e.g., "recipes").
        element_id (int): The ID of the element.

    Returns:
        dict: Element item response data from database.
    """
    config = get_main_config(element_type)

    element_data = supabase_connection.find_by(
        config["table"],
        "id",
        element_id,
    )
    if not element_data:
        logger.error(f"{element_type} with id={element_id} not found")
        raise ResourceNotFound

    return element_data[0]