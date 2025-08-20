from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.crud.entity_all_attached.post_methods import create_relationships
from api.crud.utils import pop_attributes, add_attributes


"""CREATE ELEMENT"""
async def create_element(element_type: str, element_data: dict):
    """Function creates a record in element table."""
    config = ENTITY_MAPPING[element_type]

    element_data, popped_attributes = pop_attributes(
        element_data,
        [relation["name"] for relation in config["relation"]]
    )

    element_data = supabase_connection.insert(
        config["table"],
        element_data
    )
    logger.debug(f"Element: {element_data} inserted to table {config['table']}.")
    element_id = element_data["id"]

    attributes_to_add = await create_relationships(element_type, element_id, popped_attributes)
    element_data = add_attributes(element_data, attributes_to_add)

    return element_data