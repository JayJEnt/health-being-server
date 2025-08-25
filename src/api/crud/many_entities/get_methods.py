from api.crud.nested.get_methods import get_nested
from api.crud.relation.get_methods import get_relationships_and_related_tables
from api.crud.utils import add_attributes, get_main_config
from api.handlers.exceptions import ResourceNotFound
from database.supabase_connection import supabase_connection
from logger import logger


# TODO: FIX DOCS
async def get_all(
    element_type: str,
    element_id: int,
    related_attributes: list = [],
    nested_attributes: list = [],
) -> dict:
    """Function get element by id from element table."""
    config = get_main_config(element_type)

    element_data = supabase_connection.find_by(
        config["table"],
        config["id"],
        element_id,
    )[0]
    if not element_data:
        logger.error(f"{element_type} with id={element_id} not found")
        raise ResourceNotFound

    attributes_to_add = await get_relationships_and_related_tables(element_type, element_id, related_attributes)
    attributes_to_add += await get_nested(element_type, element_id, nested_attributes)

    element_data = add_attributes(element_data, attributes_to_add)

    return element_data
