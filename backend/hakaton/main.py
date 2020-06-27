from flask import Flask
from flask import request
from marshmallow import ValidationError

from . import services
from .schemas import TypeSchema

app = Flask(__name__)


@app.route('/api/types', methods=['GET', ])
def get_types():
    return {
        'types': TypeSchema().dump(services.get_types(), many=True)
    }


@app.route('/api/types', methods=['POST', ])
def add_type():
    try:
        new_type = TypeSchema().load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    saved_type = services.create_type(new_type)
    return TypeSchema().dump(saved_type)


@app.route('/api/types/<string:name>/update', methods=['PUT', ])
def update_type(name):
    type = services.get_type(name)
    try:
        saved_type = services.update_type(type)
    except ValidationError as err:
        return err.messages, 400

    return TypeSchema().dump(saved_type)


@app.route('/api/types/<string:name>/delete', methods=['DELETE', ])
def delete_type(name: str):
    services.delete_type(name)
    return {}, 204


@app.route('/api/types/<string:name>/export/xsd', methods=['GET', ])
def export_type(name: str):
    return {

    }
