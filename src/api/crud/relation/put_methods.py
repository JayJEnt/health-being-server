from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.relation.post_methods import create_relationship
from api.crud.utils import get_relation_config
from api.handlers.exceptions import ResourceNotFound


async def update_relationships(
    element_type: str, element_id: int, related_data: list
) -> list:
    """
    Update relationships between an element and one related items.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        related_elements_list (list): The list of all lists of all elements that are related to the element table.
        (e.g., ["ingredients": ["marchewka", "pomidor"], "diet_type": ["vege", "vegan"]])

    Returns:
        list[dict]: List of related items data (with extra fields if any).
    """
    attributes_to_add = []
    for related_element_list in related_data:
        related_items = []

        relation_name, related_data = next(iter(related_element_list.items()))
        relation_config = get_relation_config(element_type, relation_name)

        try:
            await supabase_connection.delete_by(
                relation_config["join_table"],
                relation_config["join_keys"][0],
                element_id,
            )
        except ResourceNotFound:
            logger.info(
                f"No {relation_config['name']} entries found for {relation_config['join_keys'][0]}={element_id}"
            )

        for item in related_data:
            related_item = await create_relationship(
                element_type, element_id, relation_name, item
            )
            related_items.append(related_item)

        attributes_to_add.append({relation_config["name"]: related_items})

    return attributes_to_add
