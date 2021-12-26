"""
Test Tika Server requests

"""

from api.app.tika import TikaRequest, tika_parse_body


# TODO: add cassettes for HTTP calls
def test_tika_docx() -> None:
    """
    Test Docx submission for Tika server
    """

    test_doc = '../datasets/docx/statement_of_purpose.docx'
    tika_request = TikaRequest(test_doc)
    resp = tika_request.send('PUT', '/tika',)
    assert isinstance(resp.json(), dict)


def test_tika_pdf() -> None:
    """
    Test PDF parsing
    """
    test_doc = '../datasets/pdfs/5-Level Paging and 5-Level EPT - Intel - Revision 1.0 (December, 2016).pdf'
    tika_request = TikaRequest(test_doc)
    resp = tika_request.send('PUT', '/tika',)
    assert isinstance(resp.json(), dict)


def test_tika_get_text_docx() -> None:
    """
    Test text parsing from Tika server
    """
    text = tika_parse_body(
        file_path='../datasets/docx/statement_of_purpose.docx',
    )
    assert len(text) > 100


def test_tika_get_text_pdf() -> None:
    """
    Test text parsing from Tika server
    """
    text = tika_parse_body(
        file_path='../datasets/pdfs/5-Level Paging and 5-Level EPT - Intel - Revision 1.0 (December, 2016).pdf',
    )
    assert len(text) > 100
