"""
Load my resume into MongoDB

"""
from files import create_fern_doc
from models import FernDoc, FernDocName, FernDocText, FernEntities
from mongoengine import connect

database = 'fern-flask-testing'


def init_db():
    connect('graphene-mongo-example', host='mongomock://localhost', alias='default')
    path_ = '/Users/csmizzle/Documents/gt_application/statement_of_purpose.docx'
    doc = create_fern_doc(path_)
    doc.load_entities()

    f_path = FernDocName(name=path_)
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

    fern_doc.save()
