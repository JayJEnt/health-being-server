"""/images router"""

from fastapi import APIRouter, UploadFile

from api.handlers.exceptions import DemandQueryParameter
from database.s3_connection import s3


router = APIRouter(prefix="/images", tags=["public: images"])


@router.post("/download/", response_model=UploadFile)
async def download_image(recipe_id: str):
    if not recipe_id:
        raise DemandQueryParameter
    return await s3.download(recipe_id)
