"""/images router"""

from fastapi import APIRouter, UploadFile, File, Depends

from api.authentication.allowed_roles import logged_only
from api.handlers.exceptions import DemandQueryParameter
from database.s3_connection import s3


router = APIRouter(prefix="/images", tags=["user: images"])


@router.post("/upload/", response_model=None, dependencies=[Depends(logged_only)])
async def upload_image(recipe_id: int, file: UploadFile = File(...)):
    if not recipe_id:
        raise DemandQueryParameter
    await s3.upload(recipe_id, file)
