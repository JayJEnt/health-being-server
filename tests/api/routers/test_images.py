from fastapi import UploadFile

import io
import pytest

from api.routers.user_role.images import upload_image
from api.routers.public.images import download_image


@pytest.mark.asyncio
async def test_upload_image(mocked_s3_connection):
    file_content = b"fake file content"
    fake_file = UploadFile(filename="test.obj", file=io.BytesIO(file_content))

    await upload_image(1, fake_file)

    assert True


@pytest.mark.asyncio
async def test_upload_image_error(mocked_s3_connection_error):
    file_content = b"fake file content"
    fake_file = UploadFile(filename="test.obj", file=io.BytesIO(file_content))

    with pytest.raises(Exception) as e_info:
        await upload_image(1, fake_file)

    assert str(e_info.value) == "500: Internal server error"


@pytest.mark.asyncio
async def test_download_image(mocked_s3_connection):
    await download_image(1)

    assert True


@pytest.mark.asyncio
async def test_download_image_error(mocked_s3_connection_error):
    with pytest.raises(Exception) as e_info:
        await download_image(1)

    assert str(e_info.value) == "500: Internal server error"
