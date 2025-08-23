from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.handlers.exceptions import ResourceNotFound


"""DELETE ELEMENT BY ID"""
async def delete_element_by_id(element_type: str, element_id: int):
    """Function deletes a record in element table, relationship/join tables and nested tables"""
    config = ENTITY_MAPPING[element_type]

    await delete_relationships(element_type, element_id)
    await delete_nested(element_type, element_id)

    try:
        element = supabase_connection.delete_by(
            config["table"],
            "id",
            element_id
        )
    except ResourceNotFound:
        logger.info(f"{element_type} with id={element_id} not found in database")
        raise

    return element


async def delete_relationships(element_type: str, element_id: int):
    """Function delets a records in relationship/join tables"""
    config = ENTITY_MAPPING[element_type]

    for relation in config["relation"]:
        try:
            supabase_connection.delete_by(
                relation["join_table"],
                relation["join_keys"][0],
                element_id
            )
        except ResourceNotFound:
            logger.info(f"No {relation['name']} entries found for {relation['join_keys'][0]}={element_id}")


async def delete_nested(element_type: str, element_id: int):
    """Function delets a records in nested tables"""
    config = ENTITY_MAPPING[element_type]

    for nested in config["nested"]:
        try:
            supabase_connection.delete_by(
                ENTITY_MAPPING[nested["name"]]["table"],
                nested["join_key"],
                element_id
            )
        except ResourceNotFound:
            logger.info(f"No {nested["name"]} entries found for {nested["join_key"]}={element_id}")