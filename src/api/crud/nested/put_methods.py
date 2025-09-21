from api.crud.utils import get_relation_config, get_related_config
from api.handlers.http_exceptions import ResourceNotFound
from database.supabase_connection import supabase_connection
from logger import logger


async def update_nested(
    element_type: str, element_id: int, nested_data_list: list
) -> list:
    """
    Update records in nested.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        nested_data_list (dict): List of nested elements (e.g., {"ingredients": ["carrot", "ananas"]})

    Returns:
        dict: Related item data (with extra fields if any).
    """
    nested_attributes = []
    for nested_data in nested_data_list:
        nested_name, nested_item = next(iter(nested_data.items()))
        nested_config = get_relation_config(
            element_type, nested_name, relation_type="nested"
        )
        related_config = get_related_config(
            element_type, nested_name, relation_type="nested"
        )

        try:
            supabase_connection.delete_by(
                related_config["table"], nested_config["join_key"], element_id
            )
        except ResourceNotFound:
            logger.info(
                f"No {nested_config["name"]} entries found for {nested_config["join_key"]}={element_id}"
            )
            continue

        nested_item[nested_config["join_key"]] = element_id

        inserted = supabase_connection.insert(
            related_config["table"],
            nested_item,
        )
        logger.debug(
            f"Nested element: {inserted} inserted to table {related_config['table']}."
        )

        nested_attributes.append({nested_name: inserted})

    return nested_attributes
