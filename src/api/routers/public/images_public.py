"""/images router"""

from fastapi import APIRouter, UploadFile

from database.s3_connection import s3


router = APIRouter(prefix="/images", tags=["public: images"])


@router.get("/download", response_model=UploadFile)
async def download_image(recipe_id: str):
    return await s3.download(recipe_id)
