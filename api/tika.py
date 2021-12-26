"""
Class for handling Apache Tika Server Requests

"""

from requests import Request, Response, Session
from bs4 import BeautifulSoup
import traceback


class TikaRequest:
    """
    Wrapper for Tika server requests
    Set up config variables in this class for now, add this to a configuration file
    soon
    Supported file types: https://www.tutorialspoint.com/tika/tika_file_formats.htm
    """

    TIKA_HOST = 'http://localhost'
    TIKA_PORT = '1337'
    TIKA_SERVER = f"{TIKA_HOST}:{TIKA_PORT}"

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.session = Session()
        self.request = Request()

    def _set_headers(self, content_type: str = 'json') -> dict:
        """
        Parse file path and get file type
        :param content_type: str
        """
        headers = dict()

        # parse file extension
        file_extension = self.file_path.split('.')[-1]
        if file_extension == 'pdf':
            headers['Content-type'] = 'application/pdf'
        # not sure if we need to set anything for docx, will test
        if file_extension == 'docx':
            pass
        # set content type
        if content_type == 'json':
            headers['Accept'] = 'application/json'
        if content_type == 'html':
            headers['Accept'] = 'text/html'
        if content_type == 'csv':
            headers['Accept'] = 'text/csv'
        if content_type == 'plain':
            headers['Accept'] = 'text/plain'
        return headers

    def _set_request(self, content_type: str = 'json') -> None:
        """
        Prep request with params
        Ifi additional params need to be set, do it here
        """
        headers = self._set_headers(content_type)
        self.request.headers = headers
        try:
            self.request.data = open(self.file_path, 'rb')
        except FileNotFoundError:
            print(f'File {self.file_path} does not exist ...')
            traceback.print_exc()

    def send(self, method: str, endpoint: str, content_type: str = 'json') -> Response:
        """
        Send formatted request
        :param method: HTTP method
        :param endpoint: Tika endpoint
        :param content_type: accept content
        :return: Response
        """
        self._set_request(content_type)
        self.request.method = method
        self.request.url = self.TIKA_SERVER+f'/{endpoint}'
        prepped = self.request.prepare()
        return self.session.send(prepped)


def tika_parse_body(*, file_path: str) -> str:
    """
    Get body of parsed text from Tika
    :param file_path: file location

    :return: str
    """
    return BeautifulSoup(
        TikaRequest(file_path).send(
            method='PUT',
            endpoint='/tika',
        ).json()['X-TIKA:content'],
        features='lxml',
    ).get_text()
