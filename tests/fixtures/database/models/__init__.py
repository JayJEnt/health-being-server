from tests.fixtures.database.models.diet_type import DietType
from tests.fixtures.database.models.ingredient import Ingredient
from tests.fixtures.database.models.recipe import Recipe
from tests.fixtures.database.models.user import User
from tests.fixtures.database.models.vitamin import Vitamin
from tests.fixtures.database.models.joins.diet_type_included import DietTypeIncluded
from tests.fixtures.database.models.joins.ingredients_included import (
    IngredientsIncluded,
)
from tests.fixtures.database.models.joins.prefered_ingredients import (
    PreferedIngredients,
)
from tests.fixtures.database.models.joins.prefered_recipe_type import PreferedRecipeType
from tests.fixtures.database.models.joins.recipe_favourite import RecipeFavourite
from tests.fixtures.database.models.joins.refrigerator import Refrigerator
from tests.fixtures.database.models.joins.vitamins_included import VitaminsIncluded
from tests.fixtures.database.models.joins.follows import Follow

__all__ = [
    "DietType",
    "DietTypeIncluded",
    "Follow",
    "Ingredient",
    "IngredientsIncluded",
    "PreferedIngredients",
    "PreferedRecipeType",
    "Recipe",
    "RecipeFavourite",
    "Refrigerator",
    "User",
    "Vitamin",
    "VitaminsIncluded",
]
