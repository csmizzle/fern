"""
Load my resume into MongoDB

"""
import traceback

from files import create_fern_doc
from models import FernDoc, FernDocName, FernDocText, FernEntities
from mongoengine import connect
from flask import current_app

database = 'mongodb://mongo:27017/fern-flask-docker'


def doc_from_path(file_path: str) -> None:
    """
    Load doc to Fern
    :param file_path: str
    :return: None
    """
    connect(host=database, alias='default')
    try:
        current_app.logger.info(f'Ferning {file_path}...')
        doc = create_fern_doc(file_path)
        current_app.logger.info(f'Loading entities {file_path}...')
        doc.load_entities()
        f_path = FernDocName(name=file_path)
        f_path.save()
        current_app.logger.info(f'Getting text {file_path}...')
        f_text = FernDocText(text=doc.text)
        f_text.save()
        current_app.logger.info(f'Getting entities {file_path}...')
        f_entities = FernEntities(entities=doc.entity_dict)
        f_entities.save()
        current_app.logger.info(f'Creating doc {file_path}...')
        fern_doc = FernDoc(
            name=f_path,
            text=f_text,
            entities=f_entities,
        )
        current_app.logger.info(f'{file_path} entered ...')
        fern_doc.save()
    except Exception:
        current_app.logger.error(traceback.print_exc())
