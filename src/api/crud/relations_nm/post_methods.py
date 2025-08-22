from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.single_entity.get_methods import get_element_by_name
from api.crud.utils import pydantic_to_dict
from api.crud.entity_mapping import ENTITY_MAPPING
from api.handlers.exceptions import ResourceNotFound, ReferencesToItself


async def create_relationship(
    element_type: str,
    element_id: int,
    relation_name: str,
    related_data: dict
):
    """
    Create a single relationship between an element and one related item.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relation_name (str): The name of the relation (e.g., "ingredients").
        related_data (dict): Data for the related element, including identifying column and optional extra fields.

    Returns:
        dict: Related item data (with extra fields if any).
    """
    related_data = pydantic_to_dict(related_data)

    config = ENTITY_MAPPING[element_type]

    relation_config = next(
        (rel for rel in config["relation"] if rel["name"] == relation_name),
        None
    )
    if not relation_config:
        raise ValueError(f"Relation '{relation_name}' not defined for element '{element_type}'")

    # if data reference to itself drop operation with warning
    if element_type == relation_name and element_id == related_data["id"]:
        logger.error(f"Element {element_type} with id={element_id} tries to reference to itself.")
        raise ReferencesToItself

    related_config = ENTITY_MAPPING[relation_config['name']]
    related_column = related_config['column_name']

    try:
        exists = await get_element_by_name(relation_config['name'], related_data[related_column])
    except ResourceNotFound:
        logger.error(f"{relation_config['name'].capitalize()} '{related_data[related_column]}' not recognized")
        return None

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