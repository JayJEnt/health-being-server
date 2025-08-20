from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING


"""CREATE ELEMENT"""
async def create_element(element_type: str, element_data: dict):
    """Function creates a record in element table."""
    config = ENTITY_MAPPING[element_type]

    element_data = supabase_connection.insert(
        config["table"],
        element_data
    )
    logger.debug(f"Element: {element_data} inserted to table {config['table']}.")

    return element_data