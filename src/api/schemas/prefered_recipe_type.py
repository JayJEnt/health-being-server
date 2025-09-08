from pydantic import BaseModel


"""Prefered recipe type models"""


# TODO: delete in all relationships Create/PostCreate if there are no additional attributese while creating
class CreatePreferedRecipeType(BaseModel):
    diet_name: str


class PostCreatePreferedRecipeType(CreatePreferedRecipeType):
    id: int


class PreferedRecipeType(BaseModel):
    user_id: int
    type_id: int
