from pydantic import BaseModel


class RecipeFavouriteCreate(BaseModel):
    title: str


class RecipeFavouriteResponse(RecipeFavouriteCreate):
    recipe_id: int


class RecipeFavouriteDelete(BaseModel):
    user_id: int
    recipe_id: int
