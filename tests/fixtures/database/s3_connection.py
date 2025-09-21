import boto3
import moto
import pytest

from api.handlers.http_exceptions import InternalServerError
from api.routers.user_role import images_user
from api.routers.public import images_public
from database.s3_connection import S3Connection
from config import settings


@pytest.fixture()
def empty_bucket():
    with moto.mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=settings.BUCKET_NAME)
        yield s3


@pytest.fixture()
def no_bucket():
    with moto.mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        yield s3


@pytest.fixture()
def mocked_s3_connection(monkeypatch, empty_bucket):
    def __init__(self):
        self._client = empty_bucket

    monkeypatch.setattr(S3Connection, "__init__", __init__)

    test_s3_connection = S3Connection()

    monkeypatch.setattr(images_user, "s3", test_s3_connection)
    monkeypatch.setattr(images_public, "s3", test_s3_connection)


@pytest.fixture()
def mocked_s3_connection_no_bucket(monkeypatch, no_bucket):
    def __init__(self):
        self._client = no_bucket

    monkeypatch.setattr(S3Connection, "__init__", __init__)

    test_s3_connection = S3Connection()

    monkeypatch.setattr(images_user, "s3", test_s3_connection)
    monkeypatch.setattr(images_public, "s3", test_s3_connection)


@pytest.fixture
def broken_s3_connection(monkeypatch):
    class BrokenS3Client:
        def put_object(self, *args, **kwargs):
            raise InternalServerError()

        def get_object(self, *args, **kwargs):
            raise InternalServerError()

    test_s3_connection = S3Connection()
    test_s3_connection._client = BrokenS3Client()

    monkeypatch.setattr(images_user, "s3", test_s3_connection)
    monkeypatch.setattr(images_public, "s3", test_s3_connection)
