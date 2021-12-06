"""
FERN api endpoints

"""
from mongoengine import connect
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema


app = Flask(__name__)
client = connect('fern-flask-testing', alias='default')

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
    app.run()
