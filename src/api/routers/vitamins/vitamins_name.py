"""/vitamins/name/{vitamin_name} endpoint"""
from . import (
    supabase_connection,
    router,
    settings,
    Vitamin,
)


@router.get("/name/{vitamin_name}", response_model=Vitamin)
async def get_vitamin_by_name(vitamin_name: str):
    vitamin = supabase_connection.find_ilike(
        settings.VITAMIN_TABLE,
        "name",
        vitamin_name,
    )
    return vitamin[0]