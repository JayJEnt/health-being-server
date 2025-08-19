from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mappings import ENTITY_MAPPING
from api.crud.utils import pop_attributes, add_attributes
from api.handlers.exceptions import ResourceNotFound


"""GET ALL ELEMENTS"""
async def get_elements(element_type: str, restrict: bool=False):
    """Function get all records in element table."""
    config = ENTITY_MAPPING[element_type]

    elements_response = supabase_connection.fetch_all(config["table"])
    if restrict:
        elements_response = await restrict_data(element_type, elements_response)

    return elements_response


async def restrict_data(element_type: str, elements: list):
    """Function that filter data and drop restriction keys."""
    config = ENTITY_MAPPING[element_type]

    filtered_response = []
    for element in elements:
        filtered_element, popped_attributes = pop_attributes(
            element,
            [n["name"] for n in config["restricted"]]
        )
        filtered_response.append(filtered_element)

    return filtered_response




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

    attributes_to_add = await get_relationships(element_type, element_id)
    # attributes_to_add += await get_nested(element_type, element_id)
    element_data = add_attributes(element_data, attributes_to_add)
    return element_data


async def get_relationships(element_type: str, element_id: int) -> list:
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

            related_items = await get_items(relation, join_table_items)
            attributes_to_add.append({relation["name"]: related_items})

        return attributes_to_add


async def get_items(relation: dict, join_table_items: list) -> list:
    """
    Function get a items from foreign table and merge them with relationships/join table items
        Returns: list of items of 1 foreign attribute
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
                f"Couldn't find item: {relation["name"]} in {ENTITY_MAPPING[relation["name"]]["table"]}."
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


async def get_nested(element_type: str, element_id: int) -> list:
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




"""GET ELEMENT BY NAME"""
async def get_element_by_name(element_type: str, element_name: str, alternative_name: bool=False):
    """Function get a record in element table by element's name."""
    config = ENTITY_MAPPING[element_type]

    if alternative_name:
        column_name = config["alternative_column_name"]
    else:
        column_name = config["column_name"]

    elements = supabase_connection.find_ilike(
        config["table"],
        column_name,
        element_name,
    )
    if not elements or elements[0][column_name].lower()!=element_name.lower():
        raise ResourceNotFound
    return elements[0]