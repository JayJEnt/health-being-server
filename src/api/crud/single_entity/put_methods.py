from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.handlers.exceptions import ResourceNotFound


"""UPDATE ELEMENT BY ID"""
async def update_element_by_id(element_type: str, element_id: int, element_data: dict):
    """Function update a record in element table."""
    config = ENTITY_MAPPING[element_type]

    try:
        element_data = supabase_connection.update_by(
            config["table"],
            "id",
            element_id,
            element_data,
        )
        logger.debug(f"Element: {element_data} in table {config['table']} got updated.")
    except ResourceNotFound:
        logger.info(f"{element_type.capitalize()} with id={element_id} not found in database")
        raise

    return element_data