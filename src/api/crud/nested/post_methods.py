from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.single_entity.get_methods import is_duplicated
from api.crud.utils import get_relation_config, get_related_config


async def create_nested(
    element_type: str, element_id: int, nested_data_list: list
) -> list:
    """
    Create records in nested.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        nested_data_list (list): List of nested elements

    Returns:
        list: Related item data (with extra fields if any).
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

        nested_item[nested_config["join_key"]] = element_id

        await is_duplicated(nested_config["name"], element_id)

        inserted = supabase_connection.insert(
            related_config["table"],
            nested_item,
        )
        logger.debug(
            f"Nested element: {inserted} inserted to table {related_config['table']}."
        )

        nested_attributes.append({nested_name: inserted})

    return nested_attributes
