"""
Document schema

"""

import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import FernDocName as NameModel
from models import FernDocText as TextModel
from models import FernEntities as EntitiesModel
from models import FernDoc as DocModel


class DocName(MongoengineObjectType):
    class Meta:
        model = NameModel
        interfaces = (Node,)


class DocText(MongoengineObjectType):
    class Meta:
        model = TextModel
        interfaces = (Node,)


class DocEntities(MongoengineObjectType):
    class Meta:
        model = EntitiesModel
        interfaces = (Node,)


class Doc(MongoengineObjectType):
    class Meta:
        model = DocModel
        interfaces = (Node,)


class Query(graphene.ObjectType):
    node = Node.Field()
    all_documents = MongoengineConnectionField(Doc)
    all_entities = MongoengineConnectionField(DocEntities)
    all_names = MongoengineConnectionField(DocName)
    all_text = MongoengineConnectionField(DocText)


schema = graphene.Schema(query=Query, types=[
    DocName, DocText, DocEntities, Doc
])
