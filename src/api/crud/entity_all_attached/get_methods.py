from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.crud.utils import add_attributes
from api.handlers.exceptions import ResourceNotFound


"""GET ELEMENT BY ID"""
async def get_element_by_id(element_type: str, element_id: int):
    """Function get element by id from element table."""
    config = ENTITY_MAPPING[element_type]

    element_data = supabase_connection.find_by(
        config["table"],
        "id",
        element_id,
    )
    if not element_data:
        logger.error(f"{element_type} with id={element_id} not found")
        raise ResourceNotFound
    element_data = element_data[0]

    attributes_to_add = await get_relationships_and_related_tables(element_type, element_id)
    attributes_to_add += await get_nested_table_items(element_type, element_id)
    element_data = add_attributes(element_data, attributes_to_add)
    return element_data


async def get_relationships_and_related_tables(element_type: str, element_id: int) -> list:
        """
        Function get a data from relationships/join tables (N:M) to get element with it's relation attributes.
            Returns: list of attributes from foreign tables
        """
        config = ENTITY_MAPPING[element_type]

        attributes_to_add = []
        for relation in config["relation"]:
            try:
                join_table_items = supabase_connection.find_by(
                    relation["join_table"],
                    relation["join_keys"][0],
                    element_id,
                )
            except ResourceNotFound:
                logger.info(f"No {relation["name"]} found for {element_type} id={element_id}")
                attributes_to_add.append({relation["name"]: []})
                continue

            related_items = await get_related_tables_items(relation, join_table_items)
            attributes_to_add.append({relation["name"]: related_items})

        return attributes_to_add


async def get_related_tables_items(relation: dict, join_table_items: list) -> list:
    """
    Function get a items from foreign table and merge them with relationships/join table items
        Returns: list of items of 1 foreign table
    """
    items_to_add = []
    for join_table_item in join_table_items:
        try:
            related_item = supabase_connection.find_by(
                ENTITY_MAPPING[relation["name"]]["table"],
                "id",
                join_table_item[relation["join_keys"][1]],
            )
        except ResourceNotFound:
            logger.error(
                f"Couldn't find item: {relation["name"]} in {ENTITY_MAPPING[relation["name"]]["table"]}. "
                f"The previously found relationship is matching not exisiting item!"
            )
            raise
        related_item = related_item[0]

        item_data = {}
        for k, v in related_item.items():
            item_data[k] = v

        if "extra_fields" in relation:
            for field in relation["extra_fields"]:
                item_data[field] = join_table_item[field]

        items_to_add.append(item_data)
    
    return items_to_add


async def get_nested_table_items(element_type: str, element_id: int) -> list:
        """
        Function get a data from nested tables (1:1) to get element with it's relation attributes.
            Returns: list of attributes from nested tables
        """
        config = ENTITY_MAPPING[element_type]

        attributes_to_add = []
        for nested in config["nested"]:
            try:
                nested_table_items = supabase_connection.find_by(
                    ENTITY_MAPPING[nested["name"]]["table"],
                    nested["join_key"],
                    element_id,
                )[0]
            except ResourceNotFound:
                logger.info(f"No {nested["name"]} found for {element_type} id={element_id}")
                attributes_to_add.append({nested["name"]: []})
                continue

            for key, value in nested_table_items.items():
                attributes_to_add.append({key: value})

        return attributes_to_add