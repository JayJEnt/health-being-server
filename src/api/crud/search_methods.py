from logger import logger
from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.handlers.exceptions import ResourceNotFound
from api.crud.get_methods import restrict_data


"""SEARCH ELEMENTS BY PHRASE"""
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
        except ResourceNotFound:
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
        raise ResourceNotFound

    if restrict:
        found_elements = await restrict_data(element_type, found_elements)

    return found_elements