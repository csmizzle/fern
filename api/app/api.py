"""
FERN api endpoints
TODO:
    - Mongo Container
        - routing and vols
    - NGINX GraphQLi route
    - HTML uploads
        - docs_raw or something handle text and file format to place in uploads
"""

from models import DocResponse
from loaders import DocUpload
from mongoengine import connect
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from schema import schema


app = Flask(__name__)
client = connect('fern-flask-testing', alias='default')


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
