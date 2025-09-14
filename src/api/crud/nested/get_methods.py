from api.crud.utils import get_related_config, get_relation_config
from api.handlers.exceptions import ResourceNotFound
from database.supabase_connection import supabase_connection
from logger import logger


async def get_nested(
    element_type: str,
    element_id: int,
    nested_data: list,
) -> list:
    """
    Create records in nested.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        nested_data (list): The list of names of elements that from nested tables. (e.g., ["ingredients_data"])

    Returns:
        dict: Related item data (with extra fields if any).
    """
    attributes_to_add = []
    for nested_name in nested_data:
        nested_config = get_relation_config(
            element_type, nested_name, relation_type="nested"
        )
        related_config = get_related_config(
            element_type, nested_name, relation_type="nested"
        )

        try:
            nested_table_items = (await supabase_connection.find_by(
                related_config["table"],
                nested_config["join_key"],
                element_id,
            ))[0]
        except ResourceNotFound:
            logger.info(
                f"No {nested_config["name"]} found for {element_type} id={element_id}"
            )
            attributes_to_add.append({nested_config["name"]: []})
            continue

        for key, value in nested_table_items.items():
            attributes_to_add.append({key: value})

    return attributes_to_add
