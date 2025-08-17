"""/images router"""
from fastapi import APIRouter, UploadFile, File, Depends

from api.authentication.allowed_roles import logged_only
from database.s3_connection import s3


router = APIRouter(prefix="/images", tags=["images"])


"""/images/upload endpoint"""
@router.post("/upload/{recipe_id}", dependencies=[Depends(logged_only)])
async def upload_image(recipe_id: int, file: UploadFile = File(...)):
    await s3.upload(recipe_id, file)




"""/images/download/{filename} endpoint"""
@router.post("/download/{recipe_id}")
async def download_image(recipe_id: str):
    return await s3.download(recipe_id)
