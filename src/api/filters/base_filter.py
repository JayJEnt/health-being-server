from api.crud.relation.get_methods import get_relationships
from api.handlers.http_exceptions import ResourceNotFound


async def filter_followed_authors(recipes: list[dict], user_id: int) -> list:
    try:
        followed_authors = await get_relationships("user", user_id, "user")
    except ResourceNotFound:
        return []

    filtered_recipes = []
    for followed_author in followed_authors:
        followed_author_id = followed_author.get("followed_user_id")
        if not followed_author_id:
            continue
        filtered_recipes += [
            recipe for recipe in recipes if recipe["owner_id"] == followed_author_id
        ]
    return filtered_recipes


async def filter_ingredients(recipes: list[dict], user_id: int) -> list:
    try:
        ingredients = await get_relationships("user", user_id, "ingredients")
    except ResourceNotFound:
        return recipes

    filtered_recipes = []
    for recipe in recipes:
        ingredients_included = await get_relationships(
            "recipes", recipe.get("id"), "ingredients"
        )

        alergies_free = True
        for ingredient in ingredients:
            id = ingredient.get("ingredient_id")
            preference = ingredient.get("preference")

            if not id or not preference == "alergic to":
                continue

            if any([ing.get("ingredient_id") == id for ing in ingredients_included]):
                alergies_free = False
                break

        if alergies_free:
            filtered_recipes.append(recipe)

    return filtered_recipes
