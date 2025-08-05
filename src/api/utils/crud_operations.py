"""Util functions allowing basic crud operations"""
from typing import Any, List, Dict

from logger import logger
from config import settings
from database.supabase_connection import supabase_connection
from api.utils.operations_on_attributes import pop_attributes, add_attributes


own_table_name_mapping = {
    "recipe": f"{settings.recipe_table}",
    "diet_type": f"{settings.diet_type_table}",
    "ingredients": f"{settings.ingredient_table}",
}

extended_table_names_mapping = {
    "recipe": [f"{settings.ingredient_table}", f"{settings.diet_type_table}"]
}

joined_table_names_mapping = {
    "recipe": [f"{settings.ingredients_included_table}", f"{settings.diet_type_included_table}"]
}

joined_attribute_names_mapping = {
    f"{settings.ingredients_included_table}": ["recipe_id", "ingredient_id", "amount", "measure_unit"],
    f"{settings.diet_type_included_table}": ["recipe_id", "diet_type_id"]
}

async def create_element(
        element: Any,
        element_name: str,
        extended_attributes: List[str],         # TODO: also can be done by mapping
        exteded_attributes_tables: List[str],   # TODO: also can be done by mapping
        exteded_attributes_columns: list[str],  # TODO: also can be done by mapping
    ):
    """
    element - the main element you are adding.
    extended_attributes - attributes that are extend from this element model.
    exteded_attributes_tables - all tables names of extended attributes, the same order as in extended_attributes.
    """
    element, popped_attributes = pop_attributes(element, extended_attributes)

    element_response = supabase_connection.insert(
        own_table_name_mapping[element_name],
        element,
    )
    element_id = element_response["id"]
    logger.debug(
        f"Inserted element: {element_response}."
        f"To table: {own_table_name_mapping[element_name]}."
        f"Newly created element's id: {element_id}."
    )

    popped_attributes_responses = []
    for popped_attribute in popped_attributes:
        logger.debug(f"Popped attribute: {popped_attribute}.")

        popped_attribute_response = []
        if popped_attribute:
            for popped_attribute_element in popped_attribute:
                # TODO: It has to be mapping other way it need to much parameters in input and it gets messy
                extended_element = supabase_connection.find_by(
                    exteded_attributes_tables[index],
                    f"{[exteded_attributes_columns[index]]}",
                    popped_attribute_element[exteded_attributes_columns[index]],
                )[0]

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
