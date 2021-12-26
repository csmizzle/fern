"""
File loader object
Server-side object that handles upload requests

"""
from flask import Request
from load_document import doc_from_path
import os


class DocUpload(object):
    """
    Write uploaded files to uploads location and clean up once Tika is finished

    """

    UPLOAD_FOLDER = '/app/uploads'

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
            self.file_location = f'{self.UPLOAD_FOLDER}'
            self.full_path = f"{self.UPLOAD_FOLDER}/{self.file_name}"

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
