from __future__ import annotations
from typing import Any
from os import getcwd
from uuid import uuid4
from pathlib import Path
from .uconf import uconf, UserConf


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
                region_name=self.config['region_name'],
                endpoint_url=self.config['endpoint_url'],
                aws_access_key_id=self.config['aws_access_key_id'],
                aws_secret_access_key=self.config['aws_secret_access_key'])
        setattr(self, '_client', client)
        return client

    def upload(self, value: Any) -> str:
        unique_filename = f'{uuid4().hex}{Path(value.filename).suffix.lower()}'
        if value.__class__.__name__ == 'UploadFile':
            uploadobj = value.file
            content_type = value.content_type
        else:
            uploadobj = value
            content_type = value.content_type
        self.client.upload_fileobj(uploadobj, self.config['bucket'], unique_filename, ExtraArgs={
            'ACL': self.config['acl'],
            'ContentType': content_type
        })
        return f"{self.config['endpoint_url']}/{self.config['bucket']}/{unique_filename}"


class AliOSSUploader(Uploader):

    def upload(self, value: Any) -> str:
        pass


class LocalFSClient:

    def __init__(self, dir: str, url: str) -> None:
        self.dir = dir
        self.url = url
        dest = Path(getcwd()) / 'public' / self.dir
        if not dest.is_dir():
            dest.mkdir(parents=True)
        self.dest = dest

    def upload(self, value: Any) -> str:
        unique_filename = f'{uuid4().hex}{Path(value.filename).suffix.lower()}'
        if value.__class__.__name__ == 'UploadFile':
            file_location = str(self.dest / unique_filename)
            with open(file_location, "wb+") as file_object:
                file_object.write(value.file.read())
        else:
            value.save(str(self.dest / unique_filename))
        return self.url + '/public/' + self.dir + '/' + unique_filename


class LocalFSUploader(Uploader):

    @property
    def client(self) -> Any:
        if hasattr(self, '_client'):
            return getattr(self, '_client')
        client = LocalFSClient(dir=self.config['dir'], url=self.config['url'])
        setattr(self, '_client', client)
        return client

    def upload(self, value: Any) -> str:
        return self.client.upload(value)


def request_uploader(name: str) -> Uploader:
    if _uploaders.get(name):
        return _uploaders[name]
    conf = uconf()
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
        case 'localfs':
            uploader = LocalFSUploader(config)
            _uploaders[name] = uploader
            return uploader
        case _:
            raise ValueError(f"unexist uploader engine '{engine}'")
