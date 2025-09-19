from pydantic import BaseModel


class PreferedRecipeTypeCreate(BaseModel):
    diet_name: str


class PreferedRecipeTypeResponse(PreferedRecipeTypeCreate):
    type_id: int


class PreferedRecipeTypeCreateResponse(PreferedRecipeTypeCreate):
    id: int


class PreferedRecipeTypeDelete(BaseModel):
    user_id: int
    type_id: int
