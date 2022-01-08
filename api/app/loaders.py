"""
File loader object
Server-side object that handles upload requests

"""
from flask import Request, current_app
from load_document import doc_from_path
from typing import Optional
import requests
import re
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
            current_app.logger.info(f'Saving {file.filename} to uploads folder ...')

            # change chris to username based folders soon
            self.file_location = f'{UPLOAD_FOLDER}'
            self.full_path = f"{UPLOAD_FOLDER}/{self.file_name}"

            # messy change this
            if os.path.isfile(self.full_path):
                current_app.logger.info(f'File {self.full_path} already exists ...')
                return True

            file.save(self.full_path)
            current_app.logger.info(f'{file.filename} saved at {self.file_location} ...')
            return True

        return False

    def _send_to_tika(self) -> bool:
        if self._write_to_uploads():
            if self.file_location:
                current_app.logger.info(f'Reading {self.full_path} ...')
                doc_from_path(file_path=self.full_path)
                return True
        else:
            current_app.logger.info('"static_file" not in initial request ...')
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


class DocURLUpload(object):
    """
    Upload URL to download
    and place in uploads folder
    """

    _allowed_extensions = [
        '.html',
    ]

    def __init__(self, data: dict) -> None:
        self.data = data
        self.file_location = ''
        self.file_name = ''
        self.page_data = ''
        self.full_path = ''

        if 'file_type' in self.data:
            self.file_type = self.data['file_type']
        if 'file_name' in self.data:
            self.file_name = self.data['file_name']
        if 'page_data' in self.data:
            self.page_data = self.data['page_data']

    @staticmethod
    def get_response_text(url) -> Optional[str]:
        """
        If successful, get response raw text
        :param url: file_name to get
        :return: str
        """
        response = requests.get(url)
        if response.status_code == 200:
            return response.text

    def _construct_file(self) -> Optional[bool]:
        """
        Construct file from html upload

        :return:
        """
        if self.file_type:
            if self.file_type in self._allowed_extensions:
                current_app.logger.info(f'Writing {self.file_name} to uploads...')
                if not str(self.file_name).endswith('.html'):
                    self.full_path = f'{UPLOAD_FOLDER}/{self._clean_path(self.file_name+self.file_type)}'
                else:
                    self.full_path = f'{UPLOAD_FOLDER}/{self.file_name}'
                file_ = open(self.full_path, 'w')
                # response_text = self.get_response_text(self.file_name)
                if self.page_data:
                    file_.write(self.page_data)
                    file_.close()
                    return True
        return False

    @staticmethod
    def _clean_path(path: str) -> str:
        """
        Clean html paths and replace special chars with '_'

        :param path:
        :return: str
        """
        return re.sub(pattern=r'[/:]', string=path, repl='_')

    def _send_to_tika(self) -> bool:
        if self._construct_file():
            if self.full_path:
                doc_from_path(file_path=self.full_path)
                return True
        else:
            current_app.logger.info('file not in data ...')
        return False

    def process(self) -> Optional[bool]:
        """
        Upload and process a request
        :return: bool
        """
        if self._send_to_tika():
            os.remove(self.full_path)
            current_app.logger.info(f'Document {self.full_path} successfully added')
            return True
