import pathlib
import time
from typing import List

import boto3
import botocore


class Boto3Wrapper(object):
    def __init__(self, bucket_name, default_path=None):
        self.__bucket_name = bucket_name
        self.__default_path = default_path if default_path else '.'
        self.__s3c = boto3.client('s3')
        self.__s3r = boto3.resource('s3')

    @property
    def default_path(self) -> str:
        return self.__destination_folder

    @default_path.setter
    def default_path(self, value: str):
        self.__destination_folder = value

    @property
    def bucket_name(self) -> str:
        return self.__bucket_name

    @bucket_name.setter
    def bucket_name(self, value: str):
        self.__bucket_name = value

    def list_objects(self, prefix=None) -> List[str]:
        """
        List over objects in bucket
        :param prefix: Optional param to set `base directory`
        :return: List
        """
        if prefix and prefix != '.':
            return [x.key for x in self.__s3r.Bucket(self.bucket_name).objects.filter(Prefix=prefix)]
        else:
            return [x.key for x in self.__s3r.Bucket(self.bucket_name).objects.all()]

    def get(self, s3_path: str, output_path: str = None) -> None:
        """
        Get file from s3 bucket.

        :param s3_path:  key in s3 bucket
        :param output_path:
        """
        try:
            if not output_path:
                output_path = f'{self.default_path}/{pathlib.Path(s3_path).name}'
            self.__s3r.Bucket(self.bucket_name).download_file(
                s3_path, output_path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

    def upload(self, file_path, s3_path, timestamp=False, force=False):
        p = pathlib.Path(s3_path)
        if not timestamp and not force:
            if s3_path in self.list_objects(p.parent.as_posix()):
                raise Exception(f'File <{s3_path}> already exists')
        elif timestamp:
            """add timestamp"""
            s3_path = f'{p.parent if p.parent.as_posix() != "." else ""}{p.stem}_{time.strftime("%Y-%m-%d-%H-%M-%S")}{p.suffix}'
        self.__s3r.Bucket(self.bucket_name).upload_file(file_path, s3_path)
