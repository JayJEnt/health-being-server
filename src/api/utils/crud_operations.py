"""Util functions allowing basic crud operations"""
from logger import logger
from config import settings
from database.supabase_connection import supabase_connection
from api.utils.operations_on_attributes import pop_attributes, add_attributes
from api.handlers.exceptions import RescourceNotFound


ENTITY_MAPPING = {
    "recipes": {
        "table": settings.RECIPE_TABLE,         # Table name
        "column_name": "title",                 # Column name used to find by name
        "nested": [                             # All nested attributes
            {
                "name": "diet_type",
                "join_table": settings.DIET_TYPE_INCLUDED_TABLE,
                "join_keys": ("recipe_id", "diet_type_id"),
            },
            {
                "name": "ingredients",
                "join_table": settings.INGREDIENTS_INCLUDED_TABLE,
                "join_keys": ("recipe_id", "ingredient_id"),
                "extra_fields": ["amount", "measure_unit"],
            }
        ]
    },
    "ingredients": {
        "table": settings.INGREDIENT_TABLE,
        "column_name": "name",
        "nested": [
            {
                "name": "vitamins",
                "join_table": settings.VITAMINS_INCLUDED_TABLE,
                "join_keys": ("ingredient_id", "vitamin_id"),
            }
        ]
    },
    "vitamins": {
        "table": settings.VITAMIN_TABLE,
        "column_name": "name",
        "nested": []
    },
    "diet_type": {
        "table": settings.DIET_TYPE_TABLE,
        "column_name": "diet_name",
        "nested": []
    },
        "user": {
        "table": settings.USER_TABLE,
        "column_name": "username",
        "nested": []
    },
}


async def create_element(element_type: str, element_data: dict):
    config = ENTITY_MAPPING[element_type]

    element_data, popped_attributes = pop_attributes(
        element_data,
        [n["name"] for n in config["nested"]]
    )

    element_response = supabase_connection.insert(
        config["table"],
        element_data
    )
    logger.debug(f"Element: {element_response} inserted to table {config["table"]}.")
    element_id = element_response["id"]

    attributes_responses = []
    for nested_config, popped_attribute in zip(config["nested"], popped_attributes):
        attribute_responses = []
        if popped_attribute:
            for item in popped_attribute:
                try:
                    exists = await get_element_by_name(nested_config['name'], item['name'])
                except RescourceNotFound:
                    exists = None
                    logger.error(f"{nested_config['name'].capitalize()} '{item['name']}' not recognized")

                if exists:
                    join_data = {
                        nested_config["join_keys"][0]: element_id,
                        nested_config["join_keys"][1]: exists["id"]
                    }
                    if "extra_fields" in nested_config:
                        for field in nested_config["extra_fields"]:
                            join_data[field] = item[field]

                    supabase_connection.insert(nested_config["join_table"], join_data)
                    attribute_responses.append(exists)
        attributes_responses.append({nested_config["name"]: attribute_responses})

    element_response = add_attributes(element_response, attributes_responses)
    return element_response


async def delete_element(element_type: str, element_id: int):
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


async def get_element_by_id(element_type: str, element_id: int):
    config = ENTITY_MAPPING[element_type]

    element_rows = supabase_connection.find_by(
        config["table"],
        "id",
        element_id,
    )
    if not element_rows:
        raise RescourceNotFound(f"{element_type} with id={element_id} not found")
    element_data = element_rows[0]

    attributes_to_add = []

    for nested in config["nested"]:
        join_table = nested["join_table"]
        main_key = nested["join_keys"][0]
        related_key = nested["join_keys"][1]
        label = nested["name"]

        try:
            join_rows = supabase_connection.find_by(
                join_table,
                main_key,
                element_id,
            )
        except RescourceNotFound:
            logger.info(f"No {label} found for {element_type} id={element_id}")
            attributes_to_add.append({label: []})
            continue

        related_items = []
        for join_row in join_rows:
            related_id = join_row[related_key]
            nested_table = ENTITY_MAPPING[label]["table"]

            related_rows = supabase_connection.find_by(
                nested_table,
                "id",
                related_id,
            )
            if not related_rows:
                continue
            related_item = related_rows[0]

            item_data = {}
            for k, v in related_item.items():
                item_data[k] = v

            if "extra_fields" in nested:
                for field in nested["extra_fields"]:
                    item_data[field] = join_row[field]

            related_items.append(item_data)

        attributes_to_add.append({label: related_items})

    element_data = add_attributes(element_data, attributes_to_add)
    return element_data


async def get_element_by_name(element_type: str, element_name: str):
    config = ENTITY_MAPPING[element_type]
    return supabase_connection.find_ilike(
        config["table"],
        config["column_name"],
        element_name,
    )