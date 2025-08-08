"""Util functions allowing basic crud operations"""
from typing import Any, List, Dict

from logger import logger
from config import settings
from database.supabase_connection import supabase_connection
from api.utils.operations_on_attributes import pop_attributes, add_attributes


mapping_for_nested_create = {
    "recipe": {
        "table_name": settings.recipe_table,
        "nested_attributes": ["diet_type", "ingredients"],
        "diet_type_join_column": "",
        "ingredients_join_column": ""
    },
    "diet_type": {
        "table_name": settings.diet_type_table,
    },
    "ingredients": {
        "table_name": settings.ingredient_table,
    }
}

def create_element(
        element: Any,
        element_name: str,
        exteded_attributes_tables: List[str],   # TODO: also can be done by mapping
        exteded_attributes_columns: list[str],  # TODO: also can be done by mapping
    ):
    """
    Base create element method, that will be used for each create/post endpoint
    """
    # INIT
    element_dict = mapping_for_nested_create[element_name]
    element_table = element_dict.get("table_name", "")
    nested_attributes = element_dict.get("nested_attributes", [])
    
    element, popped_attributes = pop_attributes(element, nested_attributes)

    element_response = supabase_connection.insert(
        element_table,
        element,
    )
    element_id = element_response["id"]
    logger.debug(
        f"Inserted element: {element_response}."
        f"To table: {element_table}."
        f"Newly created element's id: {element_id}."
    )

    popped_attributes_responses = []
    for popped_attribute in popped_attributes:
        logger.debug(f"Popped attribute: {popped_attribute}.")

        popped_attribute_response = []
        if popped_attribute:
            for popped_attribute_element in popped_attribute:
                popped_element_table_name = mapping_for_nested_create[popped_attribute_element["name"]].get("table_name", "")
                # If there is any matching, get it
                extended_element = get_element_by_name()

                logger.debug(f"Extended element found in our database.")

                # TODO: it has to be mapping for each connection of 2 tables, there are diffrent attributes
                # supabase_connection.insert(
                #     exteded_attributes_join_tables[index],
                #     {
                #         f"{exteded_attributes_join_columns[index][0]}": element_id,
                #         f"{exteded_attributes_join_columns[index][1]}": extended_element["id"]
                #     },
                # )
                popped_attribute_response.append(popped_attribute_element)
        popped_attributes_responses.append(popped_attribute_response)

    attributes_to_add = [{f"{popped_attribute_response[exteded_attributes_columns[index]]}": popped_attribute_response}
                         for popped_attribute_response, index in popped_attributes_responses]

    element_response = add_attributes(
        element_response,
        attributes_to_add
    )
    logger.debug(f"element_response: {element_response}")

    return element_response

def get_element_by_name(element_category_name: str, element_name: str,):
    """
    Base get element by name method, that will be used for each get endpoint, which tries to reach data by name
    """
    found_element = supabase_connection.find_by(
        mapping_for_nested_create[element_category_name].get("table_name"),
        "name",
        element_name,
    )
    return found_element[0]
