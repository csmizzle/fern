"""
File loader object
Server-side object that handles upload requests

"""
from flask import Request
from load_document import doc_from_path
from typing import Optional
import os

UPLOAD_FOLDER = '/app/uploads'


class DocUpload(object):
    """
    Write uploaded files to uploads location and clean up once Tika is finished

    """

    def __init__(self, request: Request) -> None:
        self.request = request
        self.file_location = ''
        self.file_name = ''
        self.full_path = ''

    def _write_to_uploads(self) -> bool:
        if 'upload_file' in self.request.files:
            file = self.request.files['upload_file']
            self.file_name = file.filename
            print(f'Saving {file.filename} to uploads folder ...')

            # change chris to username based folders soon
            self.file_location = f'{UPLOAD_FOLDER}'
            self.full_path = f"{UPLOAD_FOLDER}/{self.file_name}"

            # messy change this
            if os.path.isfile(self.full_path):
                print(f'File {self.full_path} already exists ...')
                return True

            file.save(self.full_path)
            print(f'{file.filename} saved at {self.file_location} ...')
            return True

        return False

    def _send_to_tika(self) -> bool:
        if self._write_to_uploads():
            if self.file_location:
                doc_from_path(file_path=self.full_path)
                return True
        else:
            print('"static_file" not in initial request ...')
        return False

    def process(self) -> bool:
        """
        Upload and process a request
        :return: bool
        """
        if self._send_to_tika():
            os.remove(self.full_path)
            return True
        return False


class DocRawUpload(object):
    """
    Upload raw dta to uploads server
    """

    _allowed_extensions = [
        '.html',
    ]

    def __init__(self, data: dict) -> None:
        self.data = data
        self.file_location = ''
        self.file_name = ''
        self.full_path = ''
        if 'file_type' in self.data:
            self.file_type = self.data['file_type']
        if 'raw_data' in self.data:
            self.raw_data = self.data['raw_data']
        if 'file_name' in self.data:
            self.file_name = self.data['name']

    def _construct_file(self) -> Optional[bool]:
        """
        Construct file from html upload

        :return:
        """
        if self.file_type and self.raw_data:
            if self.file_type in self._allowed_extensions:
                print('Writing file to uploads...')
                self.full_path = f'{UPLOAD_FOLDER}/{self.file_name}{self.file_type}'
                file_ = open(self.full_path, 'w')
                file_.write(self.raw_data)
                file_.close()
                return True

    def _send_to_tika(self) -> bool:
        if self._construct_file():
            if self.full_path:
                doc_from_path(file_path=self.full_path)
                return True
        else:
            print('file not in data ...')
        return False

    def process(self) -> Optional[bool]:
        """
        Upload and process a request
        :return: bool
        """
        if self._send_to_tika():
            os.remove(self.full_path)
            return True
