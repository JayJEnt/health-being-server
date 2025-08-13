from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from botocore.exceptions import ClientError
import boto3

from api.handlers.exceptions import RescourceNotFound, InternalServerError
from config import settings
from logger import logger


router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    s3 = boto3.client("s3")
    try:
        s3.put_object(
            Bucket=settings.BUCKET_NAME,
            Key=file.filename,
            Body=await file.read(),
            ContentType=file.content_type
        )
        logger.info("File uploaded successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise RescourceNotFound
        raise InternalServerError
    
@router.post("/download/{filename}")
async def download_image(filename: str):
    s3 = boto3.client("s3")
    try:
        response = s3.get_object(Bucket=settings.BUCKET_NAME, Key=filename)
        file_content = response['Body'].read()
        return Response(
            content=file_content,
            media_type=response['ContentType'],
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise RescourceNotFound
        raise InternalServerError
