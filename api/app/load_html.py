from files import create_fern_html
import requests
from models import FernDoc, FernDocName, FernDocText, FernEntities
from mongoengine import connect

database = 'fern-flask-testing'

connect(database, alias='default')
link_ = 'https://www.reuters.com/world/us/former-us-senator-presidential-candidate-bob-dole-dies-age-98-statement-2021-12-05/'
text = requests.get(link_).text
doc = create_fern_html(text)
doc.load_entities()

f_path = FernDocName(name=link_)
f_path.save()
f_text = FernDocText(text=doc.clean_text)
f_text.save()
f_entities = FernEntities(entities=doc.entity_dict)
f_entities.save()

fern_doc = FernDoc(
    name=f_path,
    text=f_text,
    entities=f_entities,
)

fern_doc.save()
