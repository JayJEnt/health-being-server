from logger import logger
from database.supabase_connection import supabase_connection
from api.handlers.exceptions import ResourceNotFound
from api.crud.utils import restrict_data, get_main_config


# TODO: overall better searching mechanizm needed
async def search_elements(
    element_type: str, phrase: str, restrict: bool = False
) -> list:
    """
    Search a record in element table by given phrase.

    Args:
        element_type (str): The type of the element (e.g., "recipes").
        phrase (str): The searching phrase.
        restrict (bool): The optional argument, that allows to drop some of the attributes.

    Returns:
        dict: List of found element item responses data from database.
    """
    config = get_main_config(element_type)
    found_elements = []

    for search_column in config["search_columns"]:
        actual_founds = []
        try:
            actual_founds = supabase_connection.find_ilike(
                config["table"], search_column, phrase
            )
        except ResourceNotFound:
            logger.info(
                f"{element_type} with phrase={phrase} not found in column={search_column}"
            )

        if actual_founds:
            for actual_found in actual_founds:
                duplicated = False
                for found_element in found_elements:
                    if found_element["id"] == actual_found["id"]:
                        duplicated = True
                        break
                if not duplicated:
                    found_elements.append(actual_found)

    if not found_elements:
        raise ResourceNotFound

    if restrict:
        found_elements = restrict_data(element_type, found_elements)

    return found_elements
