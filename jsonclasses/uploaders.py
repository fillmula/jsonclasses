from __future__ import annotations
from typing import Any
from uuid import uuid4
from pathlib import Path
from .user_conf import user_conf


_uploaders: dict[str, Uploader] = {}


class Uploader:

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def upload(self, value: Any) -> str:
        raise Exception('please use concrete subclass of uploader')


class S3Uploader(Uploader):

    @property
    def client(self) -> Any:
        from boto3 import client as s3_client
        if hasattr(self, '_client'):
            return getattr(self, '_client')
        client = s3_client('s3',
                region_name=self.config['regionName'],
                endpoint_url=self.config['endpointURL'],
                aws_access_key_id=self.config['awsAccessKeyId'],
                aws_secret_access_key=self.config['awsSecretAccessKey'])
        setattr(self, '_client', client)
        return client

    def upload(self, value: Any) -> str:
        unique_filename = f'{uuid4().hex}{Path(value.filename).suffix.lower()}'
        self.client.upload_fileobj(value, self.config['bucket'], unique_filename, ExtraArgs={
            'ACL': self.config['acl'],
            'ContentType': value.content_type
        })
        return f"{self.config['endpointURL']}/{self.config['bucket']}/{unique_filename}"


class AliOSSUploader(Uploader):

    def upload(self, value: Any) -> str:
        pass


def request_uploader(name: str) -> Uploader:
    if _uploaders.get(name):
        return _uploaders[name]
    conf = user_conf()
    uploaders_dict = conf.get('uploaders')
    if uploaders_dict is None:
        raise ValueError(f"uploader '{name}' is undefined")
    uploader_conf = uploaders_dict.get(name)
    if uploader_conf is None:
        raise ValueError(f"uploader '{name}' is undefined")
    engine = uploader_conf.get('client')
    if engine is None:
        raise ValueError(f"undefined client engine for '{name}'")
    config = uploader_conf.get('config')
    if config is None:
        raise ValueError(f"config is not found for uploader '{name}'")
    match engine:
        case 's3':
            uploader = S3Uploader(config)
            _uploaders[name] = uploader
            return uploader
        case 'alioss':
            uploader = AliOSSUploader(config)
            _uploaders[name] = uploader
            return uploader
        case _:
            raise ValueError(f"unexist uploader engine '{engine}'")
