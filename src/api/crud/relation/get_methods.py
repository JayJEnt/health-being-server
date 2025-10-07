from api.crud.single_entity.get_methods import get_element_by_id
from api.crud.utils import (
    get_relation_config,
    get_related_config,
    pop_attributes,
    add_attributes,
)
from api.handlers.http_exceptions import ResourceNotFound
from database.supabase_connection import supabase_connection
from logger import logger


async def get_relationship(
    element_type: str,
    element_id: int,
    relation_name: str,
    relation_id: int,
    find_name: bool = False,
) -> dict:
    """
    Get single relationship between an element and one related item by their's id

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relation_name (str): The name of the relation (e.g., "ingredients").
        relation_id (int): The ID of the relation element.
        id_to_name (bool): Optional - transform id to name value.

    Returns:
        dict: Relationship item data.
    """
    relation_config = get_relation_config(element_type, relation_name)

    try:
        relation = supabase_connection.find_join_record(
            relation_config["join_table"],
            relation_config["join_keys"][0],
            element_id,
            relation_config["join_keys"][1],
            relation_id,
        )
    except ResourceNotFound:
        logger.info(
            f"No {relation_config['name']} entries found for {relation_config['join_keys'][0]}={element_id}"
        )
        raise

    if find_name:
        related = await get_element_by_id(relation_name, relation_id)
        related_config = get_related_config(element_type, relation_name)

        name = [
            {related_config["column_name"]: related[related_config["column_name"]]},
        ]
        relation, p = pop_attributes(relation, [relation_config["join_keys"][0]])
        relation = add_attributes(relation, name)

    return relation


async def get_relationships(
    element_type: str,
    element_id: int,
    relation_name: str,
    find_name: bool = False,
) -> list:
    """
    Get relationships between an element and one related item by relation item id's.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relations (list): The list of all elements that are related to the element table. (e.g., ["ingredients", "diet_type"])

    Returns:
        list: List of relationship items data.
    """
    relation_config = get_relation_config(element_type, relation_name)
    try:
        relations = supabase_connection.find_by(
            relation_config["join_table"],
            relation_config["join_keys"][0],
            element_id,
        )
    except ResourceNotFound:
        logger.info(
            f"No {relation_config['name']} entries found for {relation_config['join_keys'][0]}={element_id}"
        )
        raise

    if find_name:
        new_relations = []
        for relation in relations:
            relation_id = relation[relation_config["join_keys"][1]]
            related = await get_element_by_id(relation_name, relation_id)
            related_config = get_related_config(element_type, relation_name)

            name = [
                {related_config["column_name"]: related[related_config["column_name"]]},
            ]
            relation, p = pop_attributes(relation, [relation_config["join_keys"][0]])
            relation = add_attributes(relation, name)
            new_relations.append(relation)
        relations = new_relations

    return relations


async def get_relationships_and_related_tables(
    element_type: str,
    element_id: int,
    relations: list,
) -> list:
    """
    Function get a data from relationships/join tables (N:M) to get element with it's relation attributes.

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        relations (list): The list of all elements that are related to the element table. (e.g., ["ingredients", "diet_type"])

    Returns:
        list: List of attributes from foreign tables
    """
    attributes_to_add = []
    for relation_name in relations:
        relation_config = get_relation_config(element_type, relation_name)
        try:
            element = supabase_connection.find_by(
                relation_config["join_table"],
                relation_config["join_keys"][0],
                element_id,
            )
        except ResourceNotFound:
            logger.info(
                f"No {relation_config['name']} entries found for {relation_config['join_keys'][0]}={element_id}"
            )
            raise

        logger.debug(element)
        related_items = await get_related_tables_items(
            element_type, relation_name, element
        )
        attributes_to_add.append({relation_config["name"]: related_items})

    return attributes_to_add


async def get_related_tables_items(
    element_type: str, relation_name: str, join_table_items: list
) -> list:
    """
    Function get a items from foreign table and merge them with relationships/join table items

    Args:
        element_type (str): The type of the main element (e.g., "recipes").
        element_id (int): The ID of the main element.
        join_table_items (list): The list of element attributes retrived from join table

    Returns:
        list: List of items of 1 foreign table
    """
    items_to_add = []
    for join_table_item in join_table_items:
        related_config = get_related_config(element_type, relation_name)
        relation_config = get_relation_config(element_type, relation_name)
        try:
            related_item = supabase_connection.find_by(
                related_config["table"],
                related_config["id"],
                join_table_item[relation_config["join_keys"][1]],
            )[0]
        except ResourceNotFound:
            logger.error(
                f"Couldn't find item: {relation_config["name"]} in {related_config["table"]}. "
                f"The previously found relationship is matching not exisiting item!"
            )
            raise

        selected_attributes = relation_config["selected_attributes"]
        if selected_attributes:
            related_item = {
                attribute: related_item[attribute] for attribute in selected_attributes
            }

        item_data = dict(related_item)

        if "extra_fields" in relation_config:
            for field in relation_config["extra_fields"]:
                item_data[field] = join_table_item[field]

        items_to_add.append(item_data)

    return items_to_add
