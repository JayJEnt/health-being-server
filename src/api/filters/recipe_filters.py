from api.crud.relation.get_methods import get_relationships
from api.handlers.http_exceptions import ResourceNotFound


async def filter_by_followed_authors(recipes: list[dict], user_id: int) -> list:
    """
    Filter by follwed users

    Args:
        recipes (list): The initial recipes list found
        user_id (int): Requested user id.

    Returns:
        List of filtered recipes.
    """
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


async def filter_by_prefered_ingredients(
    recipes: list[dict], user_id: int, target_preference: str, filter_in: bool = True
) -> list:
    """
    Filter in or out recipes by users preferenced ingredients

    Args:
        recipes (list): The initial recipes list found
        user_id (int): Requested user id.
        target_preference (str): Expected value to filter by (e.g. "alergic to", "like").
        filter_in (bool): Defines if you want to filter in or out recipes with matched ingredient

    Returns:
        List of filtered recipes.
    """
    try:
        ingredients = await get_relationships("user", user_id, "ingredients")
    except ResourceNotFound:
        if filter_in:
            return []
        return recipes

    filtered_recipes = []
    for recipe in recipes:
        ingredients_included = await get_relationships(
            "recipes", recipe.get("id"), "ingredients"
        )

        desired = not filter_in
        for ingredient in ingredients:
            id = ingredient.get("ingredient_id")
            preference = ingredient.get("preference")

            if not id or not preference == target_preference:
                continue

            if any([ing.get("ingredient_id") == id for ing in ingredients_included]):
                desired = filter_in
                break

        if desired:
            filtered_recipes.append(recipe)

    return filtered_recipes


async def filter_by_prefered_diets(recipes: list[dict], user_id: int) -> list:
    """
    Filter in or out recipes by users preferenced diet types

    Args:
        recipes (list): The initial recipes list found
        user_id (int): Requested user id.

    Returns:
        List of filtered recipes.
    """
    try:
        diets = await get_relationships("user", user_id, "diet_type")
    except ResourceNotFound:
        return []

    filtered_recipes = []
    for recipe in recipes:
        diet_types_included = await get_relationships(
            "recipes", recipe.get("id"), "diet_type"
        )

        desired = False
        for diet_type in diets:
            id = diet_type.get("type_id")

            if any([diet.get("diet_type_id") == id for diet in diet_types_included]):
                desired = True
                break

        if desired:
            filtered_recipes.append(recipe)

    return filtered_recipes


async def filter_by_owned_ingredients(recipes: list[dict], user_id: int) -> list:
    # TODO: Add checking if owned quantity of ingredient is satisfing required amount
    """
    Filter in or out recipes by users owned ingredients

    Args:
        recipes (list): The initial recipes list found
        user_id (int): Requested user id.

    Returns:
        List of filtered recipes.
    """
    try:
        ingredients = await get_relationships("user", user_id, "refrigerator")
    except ResourceNotFound:
        return []

    filtered_recipes = []
    for recipe in recipes:
        ingredients_included = await get_relationships(
            "recipes", recipe.get("id"), "ingredients"
        )

        has_all = True
        for ingredient in ingredients_included:
            id = ingredient.get("ingredient_id")

            if all([ing.get("ingredient_id") != id for ing in ingredients]):
                has_all = False
                break

        if has_all:
            filtered_recipes.append(recipe)

    return filtered_recipes
