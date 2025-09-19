import pytest

from api.routers.public.images_public import download_image


@pytest.mark.asyncio
async def test_download_image(mocked_s3_connection):
    await download_image(1)

    assert True


@pytest.mark.asyncio
async def test_download_image_error(mocked_s3_connection_error):
    with pytest.raises(Exception) as e_info:
        await download_image(1)

    assert str(e_info.value) == "500: Internal server error"
