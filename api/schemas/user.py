from pydantic import BaseModel
from typing import List, Optional
from api.schemas.dietary_type import DietaryType
from api.schemas.ingredient import IngredientBase
from api.schemas.refrigerator import Refrigerator
from api.schemas.personal_data import PersonalData


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    
    ## Optional fields
    
    # followed
    favorite_recipes: Optional[List[int]] = None  # list of recipe IDs
    followed_users: Optional[List[int]] = None  # list of user IDs
    
    # personal data
    personal_data: Optional[PersonalData] = None  # e.g. age, weight, height, activity level
    
    # personal preferences
    dietary_preferences: Optional[List[DietaryType]] = None
    favorite_ingredients: Optional[List[IngredientBase]] = None
    disliked_ingredients: Optional[List[IngredientBase]] = None
    avoid_ingredients: Optional[List[IngredientBase]] = None
    
    # storage
    refrigerator: Optional[Refrigerator] = None