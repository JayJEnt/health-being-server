from pydantic import BaseModel


class RecipeFavouriteCreate(BaseModel):
    title: str


class RecipeFavouriteCreateResponse(RecipeFavouriteCreate):
    id: int
    owner_id: int
    description: str
    instructions: list[str]


class RecipeFavouriteResponse(RecipeFavouriteCreate):
    recipe_id: int


class RecipeFavouriteDelete(BaseModel):
    user_id: int
    recipe_id: int
