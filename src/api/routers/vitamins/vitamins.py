"""/vitamins endpoint"""
from typing import List

from . import (
    Depends,
    admin_only,
    supabase_connection,
    router,
    settings,
    Vitamin,
    VitaminCreate,
)


@router.get("", response_model=List[Vitamin])
async def get_vitamins():
    vitamins = supabase_connection.fetch_all(settings.VITAMIN_TABLE)
    return vitamins

@router.post("", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def create_vitamin(vitamin: VitaminCreate):
    vitamin = supabase_connection.insert(
        settings.VITAMIN_TABLE,
        vitamin.model_dump(),
    )
    return vitamin