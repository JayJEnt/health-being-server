"""/vitamins/{vitamin_id} endpoint"""
from . import (
    Depends,
    admin_only,
    supabase_connection,
    router,
    settings,
    Vitamin,
    VitaminCreate,
)


@router.get("/{vitamin_id}", response_model=Vitamin)
async def get_vitamin(vitamin_id: int):
    vitamin = supabase_connection.find_by(
        settings.VITAMIN_TABLE,
        "id",
        vitamin_id,
    )
    return vitamin[0]

@router.put("/{vitamin_id}", response_model=Vitamin, dependencies=[Depends(admin_only)])
async def update_vitamin(vitamin_id: int, vitamin: VitaminCreate):
    vitamin = supabase_connection.update_by(
        settings.VITAMIN_TABLE,
        "id",
        vitamin_id, 
        vitamin.model_dump(),
    )
    return vitamin

@router.delete("/{vitamin_id}", dependencies=[Depends(admin_only)])
async def delete_vitamin(vitamin_id: int):
    vitamin = supabase_connection.delete_by(
        settings.VITAMIN_TABLE,
        "id",
        vitamin_id,
    )
    return vitamin