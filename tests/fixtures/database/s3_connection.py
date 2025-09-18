from fastapi import UploadFile

import pytest

from api.handlers.exceptions import InternalServerError
from api.routers.user_role import images as user_images
from api.routers.public import images as public_images
from database.s3_connection import S3Connection


@pytest.fixture()
def mocked_s3_connection(monkeypatch):
    async def mock_upload(self, recipe_id: int, file: UploadFile):
        pass

    async def mock_download(self, recipe_id: int):
        pass

    monkeypatch.setattr(S3Connection, "upload", mock_upload)
    monkeypatch.setattr(S3Connection, "download", mock_download)

    test_s3_connection = S3Connection()

    monkeypatch.setattr(user_images, "s3", test_s3_connection)

    yield


@pytest.fixture()
def mocked_s3_connection_error(monkeypatch):
    async def mock_upload(self, recipe_id: int, file: UploadFile):
        raise InternalServerError

    async def mock_download(self, recipe_id: int):
        raise InternalServerError

    monkeypatch.setattr(S3Connection, "upload", mock_upload)
    monkeypatch.setattr(S3Connection, "download", mock_download)

    test_s3_connection = S3Connection()

    monkeypatch.setattr(public_images, "s3", test_s3_connection)

    yield
