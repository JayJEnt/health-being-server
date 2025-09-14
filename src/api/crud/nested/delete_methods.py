from api.crud.utils import get_related_config, get_relation_config
from api.handlers.exceptions import ResourceNotFound
from database.supabase_connection import supabase_connection
from logger import logger


async def delete_nested(
    element_type: str,
    element_id: int,
    nested_data: list,
):
    """
    Delete records of the nested tables by item id's.

    Args:
        element_type (str): The type of the main element (e.g., "ingredients").
        element_id (int): The ID of the main element as well as nested since it's 1:1 relation.
        nested_data (list): The list of names of elements that from nested tables. (e.g., ["ingredients_data"])
    """
    for nested_name in nested_data:
        nested_config = get_relation_config(
            element_type, nested_name, relation_type="nested"
        )
        related_config = get_related_config(
            element_type, nested_name, relation_type="nested"
        )
        try:
            await supabase_connection.delete_by(
                related_config["table"], nested_config["join_key"], element_id
            )
        except ResourceNotFound:
            logger.info(
                f"No {nested_config["name"]} entries found for {nested_config["join_key"]}={element_id}"
            )
