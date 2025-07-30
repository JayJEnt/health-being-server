"""/recipes/{recipe_id} endpoint"""
from fastapi import APIRouter

from api.schemas.recipe import RecipePageResponse, RecipePage
from api.routers.diet_types_name_diet_name import get_diet_by_name
from api.routers.ingredients_name_ingredient_name import get_ingredient_by_name
from api.utils.operations_on_attributes import add_attributes, pop_attributes
from database.supabase_connection import supabase_connection
from config import settings
from logger import logger


router = APIRouter()


@router.get("/recipes/{recipe_id}", response_model=RecipePageResponse)
async def get_recipe(recipe_id: int):
    recipe_response = supabase_connection.find_by(
        settings.recipe_table,
        "id",
        recipe_id,
    )
    # TODO: [OPTIMALIZATION] Consider running async
    
    try:
        diet_types_included = supabase_connection.find_by(
            settings.diet_type_included_table,
            "recipe_id",
            recipe_id,
        )
        diet_type_response = []
        if diet_types_included:
            for diet_type_included in diet_types_included:
                diet_id = diet_type_included["diet_type_id"]
                logger.debug(f"diet_id: {diet_id}")

                diet_type = supabase_connection.find_by(
                    settings.diet_type_table,
                    "id",
                    diet_id,
                )

                diet_name = diet_type[0]["diet_name"]
                logger.debug(f"diet_name: {diet_name}")
                diet_type_response.append({"diet_name": diet_name})
    except:
        logger.info(f"No diet type found for recipe_id: {recipe_id}")

    # TODO: [OPTIMALIZATION] Consider running async
    ingredients_included = supabase_connection.find_by(
        settings.ingredients_included_table,
        "recipe_id",
        recipe_id,
    )
    ingredients_response = []
    if ingredients_included:
        for ingredient_included in ingredients_included:
            ingredient_id = ingredient_included["ingredient_id"]
            logger.debug(f"ingredient_id: {ingredient_id}")

            ingredient = supabase_connection.find_by(
                settings.ingredient_table,
                "id",
                ingredient_id,
            )

            ingredient_name = ingredient[0]["name"]
            logger.debug(
                f"ingredient_name: {ingredient_name},   "
                f"amount: {ingredient_included["amount"]},  "
                f"measure_unit: {ingredient_included["measure_unit"]}"
            )
            ingredients_response.append(
                {
                    "name": ingredient_name,
                    "amount": ingredient_included["amount"],
                    "measure_unit": ingredient_included["measure_unit"]
                }
            )
            
    attributes = [{"diet_type": diet_type_response}, {"ingredients": ingredients_response}]
    recipe_response = add_attributes(
        recipe_response[0],
        attributes
    )
    return recipe_response

@router.put("/recipes/{recipe_id}", response_model=RecipePageResponse)
async def update_recipe(recipe_id: int, recipe: RecipePage):
    recipe, poped_attributes = pop_attributes(recipe, ["diet_type", "ingredients"])
    recipe_response = supabase_connection.update_by(
        settings.recipe_table,
        "id",
        recipe_id, 
        recipe,
    )
    logger.debug(f"Recipe_response: {recipe_response}.")

    try:
        supabase_connection.delete_by(
            settings.diet_type_included_table,
            "recipe_id",
            recipe_id,
        )
    except:
        pass

    try:
        diet_type_response = []
        diet_type = poped_attributes[0]
        if diet_type:
            for diet in diet_type:
                try:
                    exists = exists = await get_diet_by_name(diet["diet_name"])
                except:
                    exists = None
                    logger.error(f"Diet: {diet["diet_name"]} hasn't been recognized")
                if exists:
                    logger.debug(f"Exists: {exists}")

                    supabase_connection.insert(
                        settings.diet_type_included_table,
                        {
                            "recipe_id": recipe_id,
                            "diet_type_id": exists["id"]
                        },
                    )
                    diet_type_response.append(diet)
    except:
        pass

    try:
        supabase_connection.delete_by(
            settings.ingredients_included_table,
            "recipe_id",
            recipe_id,
        )
    except:
        pass

    ingredients_response = []
    ingredients = poped_attributes[1]
    if ingredients:
        for ingredient in ingredients:
            try:
                exists = await get_ingredient_by_name(ingredient["name"])
            except:
                exists = None
                logger.error(f"Ingredient: {ingredient["name"]} hasn't been recognized")
            if exists:
                logger.debug(f"Exists: {exists}")

                supabase_connection.insert(
                    settings.ingredients_included_table,
                    {
                        "recipe_id": recipe_id,
                        "ingredient_id": exists["id"],
                        "amount": ingredient["amount"],
                        "measure_unit": ingredient["measure_unit"]
                    },
                )
                ingredients_response.append(ingredient)

    if not ingredients_response:
        logger.error("There are no valid ingredients in this recipe.")
    attributes = ([{"diet_type": diet_type_response}, {"ingredients": ingredients_response}] 
                  if diet_type_response else [{"ingredients": ingredients_response}])
    recipe_response = add_attributes(
        recipe_response,
        attributes
    )
    logger.debug(f"recipe_response: {recipe_response}")

    return recipe_response

@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    try:
        supabase_connection.delete_by(
            settings.ingredients_included_table,
            "recipe_id",
            recipe_id,
        )
    except:
        pass

    try:
        supabase_connection.delete_by(
            settings.diet_type_included_table,
            "recipe_id",
            recipe_id,
        )
    except:
        pass

    recipe = supabase_connection.delete_by(
        settings.recipe_table,
        "id",
        recipe_id,
    )
    return recipe