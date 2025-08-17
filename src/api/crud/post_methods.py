from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.crud.get_methods import get_element_by_name
from api.crud.utils import pop_attributes, add_attributes
from api.handlers.exceptions import ResourceNotFound


"""CREATE ELEMENT"""
async def create_element(element_type: str, element_data: dict):
    """Function creates a record in element table."""
    config = ENTITY_MAPPING[element_type]

    element_data, popped_attributes = pop_attributes(
        element_data,
        [n["name"] for n in config["relation"]]
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


async def create_relationships(element_type: str, element_id: int, popped_attributes: list) -> list:
        """
        Function creates a record in relationship/join tables for each attribute that is from foreign tables.
            Returns: list of attributes from foreign tables
        """
        config = ENTITY_MAPPING[element_type]
        attributes_to_add = []
        for relation_config, popped_attribute in zip(config["relation"], popped_attributes):
            related_items = []
            if popped_attribute:
                for item in popped_attribute:
                    item_name = ENTITY_MAPPING[relation_config['name']]['column_name']
                    try:
                        exists = await get_element_by_name(relation_config['name'], item[item_name])
                    except ResourceNotFound:
                        logger.error(f"{relation_config['name'].capitalize()} '{item[item_name]}' not recognized")
                        continue

                    related_item = {**exists}
                    join_data = {
                        relation_config["join_keys"][0]: element_id,
                        relation_config["join_keys"][1]: exists["id"]
                    }
                    if "extra_fields" in relation_config:
                        for field in relation_config["extra_fields"]:
                            related_item[field] = item[field]
                            join_data[field] = item[field]

                    supabase_connection.insert(relation_config["join_table"], join_data)
                    logger.debug(f"Relation element: {join_data} inserted to table {relation_config['join_table']}.")
                    related_items.append(related_item)

            attributes_to_add.append({relation_config["name"]: related_items})

        return attributes_to_add
