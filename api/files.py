"""
Document parsers
"""

from typing import Optional, Union
from pdfminer.high_level import extract_text
import re
from nltk.corpus import stopwords
import os
import spacy
from docx import Document
from bs4 import BeautifulSoup
import magic

# try to use spacy model, if not, download needed spacy model
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print(f'Downloading Spacy models needed for {__file__}')
    os.system('python -m spacy download en_core_web_lg')
    nlp = spacy.load('en_core_web_lg')


# document extractors
class SpacyDoc:
    """
    Class for string cleaning that can inherited to all document type specific
    """
    def __init__(self):
        self.text = None
        self.nlp = nlp
        self.entity_dict = dict()

    def clean(self) -> Optional[str]:
        """
        cleaning pipeline for text
        :return: str
            cleaned text
        """

        if len(self.text) > 0:
            return re.sub(r'\n', ' ', self.text)

        return None

    def collect_tokens(self, length_threshold: int = 2) -> list:
        """
        output tokens for document
        :param length_threshold: int
            length of string to ignore in token output
        :return: list
        """

        return sorted(list(set([str(token.text).lower().strip()
                                for token in self.document.doc
                                if len(token.text.strip()) > length_threshold
                                if str(token.text).lower().strip() not in set(stopwords.words('english'))
                                ])))


class PDF(SpacyDoc):
    """
    Take text from PDF into a Spacy doc for future NLP work
    """

    def __init__(self, path: str) -> None:
        super().__init__()
        self.text = extract_text(path)
        self.clean_text = self.clean()
        self.document = self.nlp(self.clean_text)

    def load_entities(self) -> None:
        """
        Load entities from a document
        """

        for entity in self.document.ents:
            if entity.label_ not in self.entity_dict.keys():
                self.entity_dict[entity.label_] = [entity.text]
            else:
                self.entity_dict[entity.label_].append(entity.text)


class Docx(SpacyDoc):
    """
    Take text from Docx into a SpacyDoc for future NLP work
    """

    def __init__(self, path: str) -> None:
        super().__init__()
        self.docx = Document(path)
        self.text = self.extract_text()
        self.clean_text = self.clean()
        self.document = nlp(self.clean_text)

    def extract_text(self) -> str:
        text = ''
        for paragraph in self.docx.paragraphs:
            text += paragraph.text + " "  # add a space for separation

        return text

    def load_entities(self) -> None:
        """
        Load entities from a document
        """

        for entity in self.document.ents:
            if entity.label_ not in self.entity_dict.keys():
                self.entity_dict[entity.label_] = [entity.text]
            else:
                self.entity_dict[entity.label_].append(entity.text)


class HTML(SpacyDoc):
    """
    FERN HTML upload

    """

    def __init__(self, html: str) -> None:
        super().__init__()
        self.text = html
        self.clean_text = BeautifulSoup(self.text).get_text().strip()
        self.document = nlp(self.clean_text)

    def load_entities(self) -> None:
        """
        Load entities from a document
        """

        for entity in self.document.ents:
            if entity.label_ not in self.entity_dict.keys():
                self.entity_dict[entity.label_] = [entity.text]
            else:
                self.entity_dict[entity.label_].append(entity.text)


def create_fern_doc(path: str) -> Optional[Union[PDF, Docx]]:
    """
    analyze file factory function

    :param path: str
    :return: Optional[PDF, Docx]
    """

    file_type = magic.from_file(path)
    if file_type:
        if 'PDF document' in file_type:
            return PDF(path)
        if 'Microsoft Word' in file_type:
            return Docx(path)


def create_fern_html(html: str) -> Optional[HTML]:
    """
    Factory for HTML docs

    :param html:
    :return: Optional[HTML]
    """
    if len(html) > 0:
        return HTML(html)
