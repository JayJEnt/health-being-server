"""
For each of table entities, there is a config, which contatins basic informations needed for CRUD operations

Schema of entity structure:

entity_name: {
    entity table name
    entity search columns (used in search endpoints)
    entity column name (used in search by name)
    relation (N:M) entities: [
        {
            relation_entity_name (the one from other entity)
            join_table_name (the one that is used for join N:M main entity with relation entity)
            join_keys_names (the column names that are forein keys from joined entities - main and relation one)
            NOTE: important! The position of join_keys matter. First one should be main entity key, then the relation one
            extra_fields (the fields that are stored in join table e.g: amount, measure)
        }
    ]
    entity restricted attributes
}
"""
# TODO: FIX DOC
from config import settings


ENTITY_MAPPING = {
    "recipes": {
        "table": settings.RECIPE_TABLE,
        "search_columns": ["title", "description"],
        "column_name": "title",
        "id": "id",
        "relation": [
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
            },
            {
                "name": "user",
                "join_table": settings.RECIPE_FAVOURITE,
                "join_keys": ("recipe_id", "user_id"),
            }
        ],
        "nested": [],
        "restricted": ["description", "instructions"],
    },
    "ingredients": {
        "table": settings.INGREDIENT_TABLE,
        "search_columns": [],
        "column_name": "name",
        "id": "id",
        "relation": [
            {
                "name": "vitamins",
                "join_table": settings.VITAMINS_INCLUDED_TABLE,
                "join_keys": ("ingredient_id", "vitamin_id"),
            },
            {
                "name": "user",
                "join_table": settings.PREFERED_INGREDIENTS_TABLE,
                "join_keys": ("ingredient_id", "user_id"),
                "extra_fields": ["preference"],
            },
        ],
        "nested": [
            {
                "name": "ingredients_data",
                "join_key": "ingredient_id",
            }
        ],
        "restricted": [],
    },
    "vitamins": {
        "table": settings.VITAMIN_TABLE,
        "search_columns": [],
        "column_name": "name",
        "id": "id",
        "relation": [],
        "nested": [],
        "restricted": [],
    },
    "diet_type": {
        "table": settings.DIET_TYPE_TABLE,
        "search_columns": [],
        "column_name": "diet_name",
        "id": "id",
        "relation": [
            {
                "name": "user",
                "join_table": settings.PREFERED_RECIPE_TYPE_TABLE,
                "join_keys": ("type_id", "user_id"),
            },
        ],
        "nested": [],
        "restricted": [],
    },
    "user": {
        "table": settings.USER_TABLE,
        "search_columns": [],
        "column_name": "username",
        "id": "id",
        "alternative_column_name": "email",
        "relation": [
            {
                "name": "recipes",
                "join_table": settings.RECIPE_FAVOURITE,
                "join_keys": ("user_id", "recipe_id"),
            },
            {
                "name": "user",
                "join_table": settings.FOLLOW_TABLE,
                "join_keys": ("user_id", "followed_user_id"),
            },
            {
                "name": "ingredients",
                "join_table": settings.PREFERED_INGREDIENTS_TABLE,
                "join_keys": ("user_id", "ingredient_id"),
                "extra_fields": ["preference"],
            },
            {
                "name": "refrigerator",
                "join_table": settings.REFRIGERATOR_TABLE,
                "join_keys": ("user_id", "ingredient_id"),
                "extra_fields": ["amount"],
            },
            {
                "name": "diet_type",
                "join_table": settings.PREFERED_RECIPE_TYPE_TABLE,
                "join_keys": ("user_id", "type_id"),
            },
        ],
        "nested": [
            {
                "name": "user_data",
                "join_key": "user_id",
            },
        ],
        "restricted": [],
    },
    "user_data": {
        "table": settings.USER_DATA_TABLE,
        "search_columns": [],
        "column_name": "user_id",
        "id": "user_id",
        "relation": [],
        "nested": [],
        "restricted": [],
    },
    "ingredients_data": {
        "table": settings.INGREDIENT_DATA_TABLE,
        "search_columns": [],
        "column_name": "ingredient_id",
        "id": "ingredient_id",
        "relation": [],
        "nested": [],
        "restricted": [],
    },
    "refrigerator": {
        "table": settings.INGREDIENT_TABLE,
        "search_columns": [],
        "column_name": "name",
        "id": "id",
        "relation": [
            {
                "name": "user",
                "join_table": settings.REFRIGERATOR_TABLE,
                "join_keys": ("ingredient_id", "user_id"),
                "extra_fields": ["amount"],
            },
        ],
        "nested": [
            {
                "name": "ingredients_data",
                "join_key": "ingredient_id",
            }
        ],
        "restricted": [],
    }
}