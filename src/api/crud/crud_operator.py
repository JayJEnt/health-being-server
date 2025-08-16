"""Util functions allowing basic crud operations"""
from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.crud.operations_on_attributes import pop_attributes, add_attributes
from api.handlers.exceptions import RescourceNotFound


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


async def get_elements(element_type: str, restrict: bool=False):
    """Function get all records in element table."""
    config = ENTITY_MAPPING[element_type]

    elements_response = supabase_connection.fetch_all(config["table"])
    if restrict:
        elements_response = await restrict_data(element_type, elements_response)

    return elements_response


async def create_relationships(element_type: str, element_id: int, popped_attributes: list) -> list:
        """
        Function creates a record in relationship/join tables for each attribute that is from foreign tables.
            Returns: list of attributes from foreign tables
        """
        config = ENTITY_MAPPING[element_type]
        attributes_to_add = []
        for nested_config, popped_attribute in zip(config["nested"], popped_attributes):
            related_items = []
            if popped_attribute:
                for item in popped_attribute:
                    item_name = ENTITY_MAPPING[nested_config['name']]['column_name']
                    try:
                        exists = await get_element_by_name(nested_config['name'], item[item_name])
                    except RescourceNotFound:
                        logger.error(f"{nested_config['name'].capitalize()} '{item[item_name]}' not recognized")
                        continue

                    related_item = {**exists}
                    join_data = {
                        nested_config["join_keys"][0]: element_id,
                        nested_config["join_keys"][1]: exists["id"]
                    }
                    if "extra_fields" in nested_config:
                        for field in nested_config["extra_fields"]:
                            related_item[field] = item[field]
                            join_data[field] = item[field]

                    supabase_connection.insert(nested_config["join_table"], join_data)
                    logger.debug(f"Nested element: {join_data} inserted to table {nested_config['join_table']}.")
                    related_items.append(related_item)

            attributes_to_add.append({nested_config["name"]: related_items})

        return attributes_to_add


async def create_element(element_type: str, element_data: dict):
    """Function creates a record in element table."""
    config = ENTITY_MAPPING[element_type]

    element_data, popped_attributes = pop_attributes(
        element_data,
        [n["name"] for n in config["nested"]]
    )

    element_data = supabase_connection.insert(
        config["table"],
        element_data
    )
    logger.debug(f"Element: {element_data} inserted to table {config['table']}.")
    element_id = element_data["id"]

    attributes_to_add = await create_relationships(element_type, element_id, popped_attributes)
    element_data = add_attributes(element_data, attributes_to_add)

    return element_data


async def get_items(nested: dict, join_table_items: list) -> list:
    """
    Function get a items from foreign table and merge them with join table items
        Returns: list of items of 1 foreign attribute
    """
    items_to_add = []
    for join_table_item in join_table_items:
        try:
            related_item = supabase_connection.find_by(
                ENTITY_MAPPING[nested["name"]]["table"],
                "id",
                join_table_item[nested["join_keys"][1]],
            )
        except RescourceNotFound:
            logger.error(
                f"Couldn't find item: {nested["name"]} in {ENTITY_MAPPING[nested["name"]]["table"]}."
                f"The previously found relationship is matching not exisiting item!"
            )
            raise
        related_item = related_item[0]

        item_data = {}
        for k, v in related_item.items():
            item_data[k] = v

        if "extra_fields" in nested:
            for field in nested["extra_fields"]:
                item_data[field] = join_table_item[field]

        items_to_add.append(item_data)
    
    return items_to_add


async def get_relationships(element_type: str, element_id: int) -> list:
        """
        Function get a data from foreign tables to get element with it's nested attributes.
            Returns: list of attributes from foreign tables
        """
        config = ENTITY_MAPPING[element_type]

        attributes_to_add = []
        for nested in config["nested"]:
            try:
                join_table_items = supabase_connection.find_by(
                    nested["join_table"],
                    nested["join_keys"][0],
                    element_id,
                )
            except RescourceNotFound:
                logger.info(f"No {nested["name"]} found for {element_type} id={element_id}")
                attributes_to_add.append({nested["name"]: []})
                continue

            related_items = await get_items(nested, join_table_items)
            attributes_to_add.append({nested["name"]: related_items})

        return attributes_to_add


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
        raise RescourceNotFound
    element_data = element_data[0]

    attributes_to_add = await get_relationships(element_type, element_id)
    element_data = add_attributes(element_data, attributes_to_add)
    return element_data


async def update_element_by_id(element_type: str, element_id: int, element_data: dict):
    """Function update a record in element table."""
    config = ENTITY_MAPPING[element_type]

    element_data, popped_attributes = pop_attributes(
        element_data,
        [n["name"] for n in config["nested"]]
    )

    try:
        element_data = supabase_connection.update_by(
            config["table"],
            "id",
            element_id,
            element_data,
        )
        logger.debug(f"Element: {element_data} in table {config['table']} got updated.")
    except RescourceNotFound:
        logger.info(f"{element_type.capitalize()} with id={element_id} not found in database")
        raise

    await delete_relationships(element_type, element_id)
    attributes_to_add = await create_relationships(element_type, element_id, popped_attributes)
    element_data = add_attributes(element_data, attributes_to_add)

    return element_data


async def delete_relationships(element_type: str, element_id: int):
    """Function delets a record in relationship/join tables for each attribute that is nested in foreign tables."""
    config = ENTITY_MAPPING[element_type]

    for nested in config["nested"]:
        try:
            supabase_connection.delete_by(
                nested["join_table"],
                nested["join_keys"][0],
                element_id
            )
        except RescourceNotFound:
            logger.info(f"No {nested['join_table']} entries found for {nested['join_keys'][0]}={element_id}")


async def delete_element_by_id(element_type: str, element_id: int):
    """Function deletes a record in element table by element's id."""
    config = ENTITY_MAPPING[element_type]

    await delete_relationships(element_type, element_id)

    try:
        element = supabase_connection.delete_by(
            config["table"],
            "id",
            element_id
        )
    except RescourceNotFound:
        logger.info(f"{element_type.capitalize()} with id={element_id} not found in database")
        raise

    return element


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
    if not elements:
        raise RescourceNotFound
    return elements[0]


# TODO: overall better searching mechanizm needed
async def search_elements(element_type: str, phrase: str, restrict: bool=False):
    config = ENTITY_MAPPING[element_type]
    found_elements = []
    
    for search_column in config["search_columns"]:
        try:
            actual_founds = supabase_connection.find_ilike(
                config["table"],
                search_column,
                phrase
            )
        except RescourceNotFound:
            logger.info(f"{element_type.capitalize()} with phrase={phrase} not found in column={search_column}")
    
        if actual_founds:
            for actual_found in actual_founds:
                duplicated = False
                for found_element in found_elements:
                    if found_element["id"] == actual_found["id"]:
                        duplicated = True
                        break
                if not duplicated:
                    found_elements += actual_found
    
    if not found_elements:
        raise RescourceNotFound

    if restrict:
        found_elements = await restrict_data(element_type, found_elements)

    return found_elements