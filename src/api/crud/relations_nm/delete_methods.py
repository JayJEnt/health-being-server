from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.handlers.exceptions import ResourceNotFound



async def delete_relationship(element_type: str, element_id: int, relation_name: str, relation_id: int):
    """Function delets a records in relationship/join tables"""
    config = ENTITY_MAPPING[element_type]

    relation_config = next(
        (rel for rel in config["relation"] if rel["name"] == relation_name),
        None
    )
    if not relation_config:
        raise ValueError(f"Relation '{relation_name}' not defined for element '{element_type}'")
    
    try:
        element = supabase_connection.delete_join_record(
            relation_config["join_table"],
            relation_config["join_keys"][0],
            element_id,
            relation_config["join_keys"][1],
            relation_id,
        )
    except ResourceNotFound:
        logger.info(f"No {relation_config['name']} entries found for {relation_config['join_keys'][0]}={element_id}")
        raise

    return element