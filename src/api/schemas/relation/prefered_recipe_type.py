from pydantic import BaseModel


"""Prefered recipe type models"""


class CreatePreferedRecipeType(BaseModel):
    diet_name: str


class PostCreatePreferedRecipeType(CreatePreferedRecipeType):
    id: int


class PreferedRecipeType(BaseModel):
    user_id: int
    type_id: int


class PreferedRecipeTypeGet(BaseModel):
    users: str
    diet_types: str
