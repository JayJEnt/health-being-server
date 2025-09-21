from fastapi import UploadFile
import pytest

import io

from api.routers.user_role.images_user import upload_image


@pytest.mark.asyncio
async def test_upload_image(mocked_s3_connection):
    file_content = b"fake file content"
    fake_file = UploadFile(filename="test.obj", file=io.BytesIO(file_content))

    await upload_image(1, fake_file)

    assert True


@pytest.mark.asyncio
async def test_upload_image_no_bucket(mocked_s3_connection_no_bucket):
    file_content = b"fake file content"
    fake_file = UploadFile(filename="test.obj", file=io.BytesIO(file_content))

    with pytest.raises(Exception) as e_info:
        await upload_image(1, fake_file)

    assert (
        str(e_info.value)
        == "An error occurred (NoSuchBucket) when calling the PutObject operation: The specified bucket does not exist"
    )
