from typing import Optional

from pydantic import BaseModel


class RecipeFilter(BaseModel):
    allergies_off: Optional[bool] = False
    liked_and_favourite_ingredients: Optional[bool] = False
    only_favourite_ingredients: Optional[bool] = False
    only_favourite_diets: Optional[bool] = False
    only_followed_authors: Optional[bool] = False
    only_owned_ingredients: Optional[bool] = False
