"""
For each of table entities, there is a config, which contatins basic informations needed for CRUD operations

Schema of entity structure:

entity_name: {
    entity table name
    entity search columns (used in search endpoints)
    entity column name (used in search by name)
    nested entities: [
        {
            nested_entity_name (the one from other entity)
            join_table_name (the one that is used for join N:M main entity with nested entity)
            join_keys_names (the column names that are forein keys from joined entities - main and nested one)
            NOTE: important! The position of join_keys matter. First one should be main entity key, then the nested one
            extra_fields (the fields that are stored in join table e.g: amount, measure)
        }
    ]
    entity restricted attributes
}
"""
from config import settings


ENTITY_MAPPING = {
    "recipes": {
        "table": settings.RECIPE_TABLE,
        "search_columns": ["title", "description"],
        "column_name": "title",
        "nested": [
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
        ],
        "restricted": ["description", "instructions"],
    },
    "ingredients": {
        "table": settings.INGREDIENT_TABLE,
        "search_columns": [],
        "column_name": "name",
        "nested": [
            {
                "name": "vitamins",
                "join_table": settings.VITAMINS_INCLUDED_TABLE,
                "join_keys": ("ingredient_id", "vitamin_id"),
            }
        ],
        "restricted": [],
    },
    "vitamins": {
        "table": settings.VITAMIN_TABLE,
        "search_columns": [],
        "column_name": "name",
        "nested": [],
        "restricted": [],
    },
    "diet_type": {
        "table": settings.DIET_TYPE_TABLE,
        "search_columns": [],
        "column_name": "diet_name",
        "nested": [],
        "restricted": [],
    },
    "user": {
        "table": settings.USER_TABLE,
        "search_columns": [],
        "column_name": "username",
        "alternative_column_name": "email",
        "nested": [],
        "restricted": [],
    },
}