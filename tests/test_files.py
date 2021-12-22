"""
Test files

"""

from api.files import DocPipe, PDFPipe


def test_text_chunking() -> None:
    """
    Test text chunking for DocPipe

    :return:
    """
    test_string = 'Chris  ' * 2000003
    pipe = DocPipe(test_string)
    chunks = pipe.chunk_texts()
    assert len(chunks) == 15


def test_pdf_pipe() -> None:
    """
    Test pdf pipe
    """
    test_path = '../datasets/pdfs/Intel 64 and IA-32 Architectures Optimization Reference Manual - December 2017 (248966-039).pdf'
    pipe = PDFPipe(test_path)
    print(pipe.load_entities())

