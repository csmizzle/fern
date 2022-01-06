"""
FERN api endpoints
TODO:
    - HTML uploads
        - docs_raw or something handle text and file format to place in uploads
"""

from models import DocResponse
from loaders import DocUpload, DocURLUpload
from mongoengine import connect
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
import json
from schema import schema
import logging


app = Flask(__name__)

logging.basicConfig(
    filename='/app/api.log',
    level=logging.DEBUG,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

client = connect(host='mongodb://mongo:27017/fern-flask-docker', alias='default')


@app.route('/doc_file', methods=["GET", "POST", "PUT"])
def doc_endpoint():
    """
    Submit documents for

    :return: DocResponse
    """

    if request.method == "PUT":
        if 'upload_file' in request.files:
            print('Received doc file ...')
            loader = DocUpload(request)
            if loader.process():
                message = 'File successfully loaded into Fern'
            else:
                message = 'File unsuccessfully loaded into Fern'
            return jsonify(
                DocResponse(
                    message=message
                ).dict()
            )


@app.route('/doc_raw', methods=['PUT', 'POST'])
def doc_raw_endpoint():
    """
    Raw text into specified format on upload server
    """
    message = ''
    if request.method == "PUT":
        data = json.loads(request.json)
        app.logger.info(f'Data: {data.keys()}')
        if 'file_type' and 'file_name' in data:
            loader = DocURLUpload(data)
            if loader.process():
                message = 'File successfully loaded into Fern'
        else:
            message = 'File unsuccessfully loaded into Fern'
    return jsonify(
        DocResponse(
            message=message
        ).dict()
    )

# add graphql view
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    )
)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
