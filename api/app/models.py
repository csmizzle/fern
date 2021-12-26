"""
MongoDB models

"""
from pydantic import BaseModel
from mongoengine import Document
from mongoengine.fields import (
    DictField,
    StringField,
    ReferenceField
)


# mongo models
class FernDocName(Document):
    meta = {'collection': 'doc_name'}
    name = StringField()


class FernDocText(Document):
    meta = {'collection': 'doc_text'}
    text = StringField()


class FernEntities(Document):
    meta = {'collection': 'doc_entities'}
    entities = DictField()


class FernDoc(Document):
    meta = {"collection": "fern_doc"}
    name = ReferenceField(FernDocName)
    text = ReferenceField(FernDocText)
    entities = ReferenceField(FernEntities)


# Flask Models
class DocResponse(BaseModel):
    message: str
