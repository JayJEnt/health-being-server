from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.single_entity.get_methods import get_element_by_name
from api.crud.utils import pydantic_to_dict, get_relation_config, get_related_config
from api.handlers.exceptions import ResourceNotFound


async def create_relationship(
    element_type: str,
    element_id: int,
    relation_name: str,
    related_data: dict
) -> dict:
    """
    Update a single relationship between an element and one related item.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relation_name (str): The name of the relation (e.g., "ingredients").
        related_data (dict): Data for the related element, including identifying column and optional extra fields.

    Returns:
        dict: Related item data (with extra fields if any).
    """
    # Get required configs
    related_data = pydantic_to_dict(related_data)
    relation_config = get_relation_config (element_type, relation_name)
    related_config = get_related_config(element_type, relation_name)
    
    # Delete relationship
    try:
        supabase_connection.delete_join_record(
            relation_config["join_table"],
            relation_config["join_keys"][0],
            element_id,
            relation_config["join_keys"][1],
            related_data["id"],
        )
    except ResourceNotFound:
        logger.info(f"No {relation_config['name']} entries found for {relation_config['join_keys'][0]}={element_id}")
        raise

    # Get full element data out of name TODO: Change pydantic models and whole infra to pass id's? To be consider
    try:
        exists = await get_element_by_name(relation_config['name'], related_data[related_config['column_name']])
    except ResourceNotFound:
        logger.error(f"{relation_config['name']} '{related_data[related_config['column_name']]}' not recognized")
        return None

    # Create data to insert
    related_item = {**exists}
    join_data = {
        relation_config["join_keys"][0]: element_id,
        relation_config["join_keys"][1]: exists["id"]
    }
    if "extra_fields" in relation_config:
        for field in relation_config["extra_fields"]:
            if field in related_data:
                related_item[field] = related_data[field]
                join_data[field] = related_data[field]

    supabase_connection.insert(relation_config["join_table"], join_data)
    logger.debug(f"Relation element: {join_data} inserted to table {relation_config['join_table']}.")

    return join_data