from database.supabase_connection import supabase_connection
from api.crud.entity_mapping import ENTITY_MAPPING
from api.handlers.exceptions import ResourceNotFound
from api.crud.utils import restrict_data
from logger import logger



"""GET ALL ELEMENTS"""
async def get_elements(element_type: str, restrict: bool=False):
    """
    Function get all records in element table.
    restrict is optional and allows to drop attributes from list in ENTITY_MAPPING.
    """
    config = ENTITY_MAPPING[element_type]

    elements_response = supabase_connection.fetch_all(config["table"])
    if restrict:
        elements_response = restrict_data(element_type, elements_response)

    return elements_response




"""GET ELEMENT BY NAME"""
async def get_element_by_name(element_type: str, element_name: str, alternative_name: bool=False):
    """
    Function get a record in element table by element's name.
    alternative_name is optional and allows to pick diffrent search column, which is stored in ENTITY_MAPPING
    """
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
        logger.error(f"{element_type} with name={element_name} not found")
        raise ResourceNotFound
    return elements[0]




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

    return element_data[0]