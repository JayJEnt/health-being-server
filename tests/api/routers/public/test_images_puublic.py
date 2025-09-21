from fastapi import UploadFile
import pytest

import io

from api.handlers.http_exceptions import InternalServerError, ResourceNotFound
from api.routers.public.images_public import download_image
from api.routers.user_role.images_user import upload_image


@pytest.mark.asyncio
async def test_download_image(mocked_s3_connection):
    file_content = b"fake file content"
    fake_file = UploadFile(filename="test.obj", file=io.BytesIO(file_content))

    await upload_image(1, fake_file)
    response = await download_image(1)

    assert response.body == file_content


@pytest.mark.asyncio
async def test_download_image_no_key(mocked_s3_connection):
    with pytest.raises(ResourceNotFound):
        await download_image(1)


@pytest.mark.asyncio
async def test_download_image_runtime_error(broken_s3_connection):
    with pytest.raises(InternalServerError):
        await download_image(1)
