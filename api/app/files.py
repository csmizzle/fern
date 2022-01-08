"""
Document parsers
"""
from flask import current_app
from tika import tika_parse_body
from typing import Optional
from math import ceil
import re
import os
import spacy
from bs4 import BeautifulSoup

# try to use spacy model, if not, download needed spacy model
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print(f'Downloading Spacy models needed for {__file__}')
    os.system('python -m spacy download en_core_web_lg')
    nlp = spacy.load('en_core_web_lg')


# Spacy Document Pipeline
class DocPipe:

    def __init__(
            self,
            text: str,
            default_length: int = 10000,
            disable_tags: list = None,
            pipeline: list = None,
    ) -> None:
        if disable_tags is None:
            disable_tags = [
                "tok2vec",
                "tagger",
                "parser",
                "attribute_ruler",
                "lemmatizer"
            ]
        self.text = text
        self.default_length = default_length
        self.pipeline = pipeline
        self.disable_tags = disable_tags
        self.nlp = nlp
        self.entity_dict = dict()

    def chunk_texts(self) -> list:
        """
        Chunk based on default_length
        :return:
        """
        if len(self.text) > self.default_length:
            chunks = ceil(len(self.text) / self.default_length)
            chunk_size = ceil(len(self.text)/chunks)
            texts = [
                self.text[i:i+chunk_size] for i in range(0, len(self.text), chunk_size)
            ]
        else:
            texts = [self.text]
        return texts

    @staticmethod
    def clean(texts) -> Optional[list]:
        """
        Clean texts
        """
        if len(texts) > 0:
            for idx, text in enumerate(texts):
                texts[idx] = re.sub(r'\n', ' ', text)
        return None

    def load_entities(self) -> None:
        """
        Collect entity stream from spacy pipeline
        :return: list
        """
        current_app.logger.info('Chunking texts ...')
        texts = self.chunk_texts()
        current_app.logger.info(f'Doc Length: {len(texts)}')
        current_app.logger.info('Iterating over entities ...')
        for idx, text in enumerate(self.nlp.pipe(
                texts,
                disable=self.disable_tags
        )):
            for ent in text.doc.ents:
                if ent.label_ not in self.entity_dict.keys():
                    self.entity_dict[ent.label_] = set(ent.text)
                else:
                    self.entity_dict[ent.label_].add(ent.text)
        current_app.logger.info('Creating entity dict ...')
        for _ in self.entity_dict.keys():
            self.entity_dict[_] = list(self.entity_dict[_])


class TikaPipe(DocPipe):
    def __init__(self, path: str) -> None:
        self.text = tika_parse_body(file_path=path)
        super().__init__(text=self.text)


# functions for classes above
def create_fern_doc(path: str) -> Optional[TikaPipe]:
    """
    analyze file factory function

    :param path: str
    :return: Optional[PDF, Docx]
    """
    if path:
        return TikaPipe(path)

