from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.crud.utils import pop_attributes, add_attributes
from api.crud.single_entity.get_methods import get_element_by_name
from api.handlers.exceptions import ResourceNotFound


"""UPDATE ELEMENT BY ID"""
async def update_element_by_id(element_type: str, element_id: int, element_data: dict):
    """Function update a record in element table."""
    config = ENTITY_MAPPING[element_type]

    element_data, popped_attributes = pop_attributes(
        element_data,
        [n["name"] for n in config["relation"]]
    )

    try:
        element_data = supabase_connection.update_by(
            config["table"],
            "id",
            element_id,
            element_data,
        )
        logger.debug(f"Element: {element_data} in table {config['table']} got updated.")
    except ResourceNotFound:
        logger.info(f"{element_type} with id={element_id} not found in database")
        raise

    attributes_to_add = await update_relationships(element_type, element_id, popped_attributes)
    element_data = add_attributes(element_data, attributes_to_add)

    return element_data


async def update_relationships(element_type: str, element_id: int, popped_attributes: list) -> list:
        """
        Function creates a record in relationship/join tables for each attribute that is from foreign tables.
            Returns: list of attributes from foreign tables
        """
        config = ENTITY_MAPPING[element_type]
        attributes_to_add = []
        for relation, popped_attribute in zip(config["relation"], popped_attributes):
            related_items = []
            try:
                supabase_connection.delete_by(
                    relation["join_table"],
                    relation["join_keys"][0],
                    element_id
                )
            except ResourceNotFound:
                logger.info(f"No {relation['name']} entries found for {relation['join_keys'][0]}={element_id}")

            if popped_attribute:
                for item in popped_attribute:
                    item_name = ENTITY_MAPPING[relation['name']]['column_name']
                    try:
                        exists = await get_element_by_name(relation['name'], item[item_name])
                    except ResourceNotFound:
                        logger.error(f"{relation['name']} '{item[item_name]}' not recognized")
                        continue

                    related_item = {**exists}
                    join_data = {
                        relation["join_keys"][0]: element_id,
                        relation["join_keys"][1]: exists["id"]
                    }
                    if "extra_fields" in relation:
                        for field in relation["extra_fields"]:
                            related_item[field] = item[field]
                            join_data[field] = item[field]

                    supabase_connection.insert(relation["join_table"], join_data)
                    logger.debug(f"Relation element: {join_data} inserted to table {relation['join_table']}.")
                    related_items.append(related_item)

            attributes_to_add.append({relation["name"]: related_items})

        return attributes_to_add
