from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.handlers.exceptions import ResourceNotFound


"""DELETE ELEMENT BY ID"""
async def delete_element_by_id(element_type: str, element_id: int):
    """Function deletes a record in element table"""
    config = ENTITY_MAPPING[element_type]

    try:
        element = supabase_connection.delete_by(
            config["table"],
            "id",
            element_id
        )
    except ResourceNotFound:
        logger.info(f"{element_type.capitalize()} with id={element_id} not found in database")
        raise

    return element