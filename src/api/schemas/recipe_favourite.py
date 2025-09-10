from pydantic import BaseModel


"""Recipe favourite models"""


class CreateRecipeFavourite(BaseModel):
    title: str


class PostCreateRecipeFavourite(BaseModel):
    id: int


class RecipeFavourite(BaseModel):
    user_id: int
    recipe_id: int
