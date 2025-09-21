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
                logger.info("Sucesfully processed.")
                return result
            except ClientError as e:
                if e.response["Error"]["Code"] == "NoSuchKey":
                    raise ResourceNotFound
                logger.error(f"S3 client error: {e}")
                raise
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
            ContentType=file.content_type or "application/octet-stream",
        )

    @error_handler
    async def download(self, recipe_id: int):
        response = self._client.get_object(
            Bucket=settings.BUCKET_NAME, Key=f"img_{recipe_id}"
        )
        file_content = response["Body"].read()
        return Response(
            content=file_content,
            media_type=response["ContentType"],
            headers={"Content-Disposition": f"attachment; filename=img_{recipe_id}"},
        )


s3 = S3Connection()
