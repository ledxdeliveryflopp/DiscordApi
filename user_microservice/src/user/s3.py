import os
from dataclasses import dataclass

import boto3
import pyshorteners

from src.settings.settings import settings


@dataclass
class S3Service:
    """Сервис S3"""
    secret_access_key: str = settings.s3_settings.secret_access_key
    secret_key_id: str = settings.s3_settings.secret_key_id

    async def __get_url_to_file_in_s3(self, file_key: str, backed_name: str = "discordapi") -> str:
        """Сделать url к файлу в S3"""
        session = boto3.session.Session()
        url_shortener = pyshorteners.Shortener()
        s3_client = session.client(
            service_name="s3",
            endpoint_url='https://storage.yandexcloud.net',
            aws_secret_access_key=self.secret_access_key,
            aws_access_key_id=self.secret_key_id
        )
        url = s3_client.generate_presigned_url("get_object", Params={"Bucket": backed_name, "Key": file_key})
        tiny_url = url_shortener.tinyurl.short(url)
        return tiny_url

    async def upload_file_in_s3(self, filename: str, backed_name: str = "discordapi") -> str:
        """Загрузить изображение в S3"""
        session = boto3.session.Session()
        s3_client = session.client(
            service_name="s3",
            endpoint_url='https://storage.yandexcloud.net',
            aws_secret_access_key=self.secret_access_key,
            aws_access_key_id=self.secret_key_id
        )
        file_path = f"temp/{filename}"
        s3_client.upload_file(file_path, backed_name, filename)
        file_url = await self.__get_url_to_file_in_s3(filename)
        os.remove(file_path)
        return file_url


s3_service = S3Service()
