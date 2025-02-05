import os
from minio import Minio
from app.settings import get_settings


Settings = get_settings()

MinioClient = Minio(
    Settings.Storage.minio.host,
    access_key=Settings.Storage.minio.access_key,
    secret_key=Settings.Storage.minio.secret_key,
    secure=Settings.Storage.minio.secure,
)

found = MinioClient.bucket_exists(os.environ["MINIO_BUCKET"])
if not found:
    MinioClient.make_bucket(os.environ["MINIO_BUCKET"])
