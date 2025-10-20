from typing import List

from api.crud.single_entity.get_methods import get_element_by_name
from api.schemas.recipe import RecipeResponseGet
from api.schemas.utils import Micronutrients, MicronutrientsTotal, MeasureUnit
from logger import logger


def micronutrients_summary(
    ingredients: List[MicronutrientsTotal],
) -> MicronutrientsTotal:
    micronutrients = MicronutrientsTotal()
    micronutrients_keys = MicronutrientsTotal.model_fields.keys()

    for ingredient in ingredients:
        ingredient_data = ingredient.model_dump()
        for key, value in ingredient_data.items():
            if key in micronutrients_keys:
                current_value = getattr(micronutrients, key, 0.0)
                setattr(micronutrients, key, current_value + (value or 0.0))

    logger.debug(f"Total micronutrients of all ingredients: {micronutrients}")

    return micronutrients


def scale_micronutrients(
    amount: float,
    measure_unit: MeasureUnit,
    rho: float,
    default_weight: float,
    micronutrients: Micronutrients,
) -> MicronutrientsTotal:
    if measure_unit in ["kg.", "l."]:
        amount *= 1000
        measure_unit = "g." if measure_unit == "kg." else "ml."

    if measure_unit == "ml.":
        measure_unit = "g."
        amount *= rho

    if measure_unit == "":
        measure_unit = "g."
        amount *= default_weight

    if measure_unit != "g.":
        raise ValueError("Unknown measure unit!")

    total = MicronutrientsTotal()

    for key, value in micronutrients.items():
        if key.endswith("_per_100"):
            base_key = key.replace("_per_100", "")
            setattr(total, base_key, (value or 0.0) * amount / 100.0)

    logger.debug(f"Total micronutrients of processed ingredient: {total}")

    return total


async def update_recipe_with_micronutrients(
    recipe: RecipeResponseGet,
) -> RecipeResponseGet:
    micronutrients_ingredients = []
    for ingredient in recipe.get("ingredients"):
        amount = ingredient.get("amount")
        measure_unit = ingredient.get("measure_unit")
        ingredient_obj = await get_element_by_name(
            "ingredients", ingredient.get("name")
        )
        rho = ingredient_obj.get("rho")
        default_weight = ingredient_obj.get("default_weight")
        micronutrients_total = scale_micronutrients(
            amount, measure_unit, rho, default_weight, ingredient_obj
        )
        micronutrients_ingredients.append(micronutrients_total)

    micronutrients: MicronutrientsTotal = micronutrients_summary(
        micronutrients_ingredients
    )
    recipe["micronutrients"] = micronutrients

    return recipe
