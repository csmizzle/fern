"""
Load my resume into MongoDB

"""
from api.files import create_fern_doc
from api.models import FernDoc, FernDocName, FernDocText, FernEntities
from mongoengine import connect

database = 'fern-flask-testing'


def doc_from_path(file_path: str) -> None:
    """
    Load doc to Fern
    :param file_path: str
    :return: None
    """
    connect(database, alias='default')
    print(f'Ferning {file_path}...')
    doc = create_fern_doc(file_path)
    doc.load_entities()
    f_path = FernDocName(name=file_path)
    f_path.save()
    f_text = FernDocText(text=doc.text)
    f_text.save()
    f_entities = FernEntities(entities=doc.entity_dict)
    f_entities.save()
    fern_doc = FernDoc(
        name=f_path,
        text=f_text,
        entities=f_entities,
    )
    print(f'{file_path} entered ...')
    fern_doc.save()
