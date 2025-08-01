"""/register endpoint"""
from fastapi import APIRouter

from src.api.schemas.user import UserCreate, User
from src.authentication.hash_methods import hash_password
from src.api.utils.operations_on_attributes import pop_attributes, add_attributes
from src.api.handlers.exceptions import RescourceAlreadyTaken, RescourceNotFound
from src.database.supabase_connection import supabase_connection
from src.config import settings
from src.logger import logger


router = APIRouter()


@router.post("/register", response_model=User)
async def create_user(user: UserCreate):
    if is_attribute_taken(user.email, "email"):
        raise RescourceAlreadyTaken
    
    user, password = pop_attributes(user, ["password"])
    hashed_password = hash_password(password[0])
    user = add_attributes(user, [{"hashed_password": hashed_password},{"role": "user"}])
    
    user = supabase_connection.insert(
        settings.user_table,
        user,
    )
    return user

# TODO: move it to some utils or whatever
def is_attribute_taken(attribute: str, attribute_name: str):
    try:
        attribute = supabase_connection.find_by(
            settings.user_table,
            f"{attribute_name}",
            attribute
        )
        if attribute[0] != None:
            return True
    except RescourceNotFound:
        return False