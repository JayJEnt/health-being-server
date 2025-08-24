from pydantic import BaseModel


"""Recipe favourite models"""
class CreateRecipeFavourite(BaseModel):
    name: str
