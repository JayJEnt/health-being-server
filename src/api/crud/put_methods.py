from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.crud.utils import pop_attributes, add_attributes
from api.crud.post_methods import create_relationships
from api.crud.delete_methods import delete_relationships
from api.handlers.exceptions import ResourceNotFound


"""UPDATE ELEMENT BY ID"""
async def update_element_by_id(element_type: str, element_id: int, element_data: dict):
    """Function update a record in element table."""
    config = ENTITY_MAPPING[element_type]

    element_data, popped_attributes = pop_attributes(
        element_data,
        [n["name"] for n in config["relation"]]
    )

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

    await delete_relationships(element_type, element_id)
    attributes_to_add = await create_relationships(element_type, element_id, popped_attributes)
    element_data = add_attributes(element_data, attributes_to_add)

    return element_data