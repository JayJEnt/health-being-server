from botocore.exceptions import ClientError
import boto3
from fastapi import UploadFile
from fastapi.responses import Response

from functools import wraps

from api.handlers.exceptions import ResourceNotFound, InternalServerError
from config import settings
from logger import logger


class S3Connection:
    def __init__(self):
        self._client = boto3.client("s3")

    @staticmethod
    def error_handler(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                logger.info(f"Processing request: {func.__name__}")
                result = await func(*args, **kwargs)
                if func.__name__ == "download" and result is None:
                    func_args = args[1:] if args and args[0].__class__.__name__ == "S3Connection" else args
                    logger.info(
                        f"Resource not found - Operation: {func.__name__}, "
                        f"Args: {func_args}"
                    )
                    raise ResourceNotFound
                logger.info(f"Sucesfully processed.")
                return result
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchKey':
                    raise ResourceNotFound
                logger.error(f"S3 client error: {e}")
            except Exception as ex:
                logger.error(f"S3 error: {ex}")
                raise InternalServerError
        return wrapper
    
    @error_handler
    async def upload(self, recipe_id: int, file: UploadFile):
        file_content = await file.read()
        self._client.put_object(
            Bucket=settings.BUCKET_NAME,
            Key=f"img_{recipe_id}",
            Body=file_content,
            ContentType=file.content_type
        )

    @error_handler
    async def download(self, recipe_id: int):
        response = self._client.get_object(Bucket=settings.BUCKET_NAME, Key=f"img_{recipe_id}")
        file_content = response['Body'].read()
        return Response(
            content=file_content,
            media_type=response['ContentType'],
            headers={"Content-Disposition": f"attachment; filename=img_{recipe_id}"}
        )
    

s3 = S3Connection()