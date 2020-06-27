from flask import Flask
from flask import request, Response

from . import services


app = Flask(__name__)


@app.route('/api/types', methods=['GET', ])
def get_types():
    return {
        'types': [
            {
                'name': 'string',
            },
            {
                'name': 'integer',
            },
        ]
    }


@app.route('/api/types', methods=['POST', ])
def add_type():
    type = request.get_json()
    return services.create_type(type)


@app.route('/api/types/<str:name>', methods=['PUT', ])
def update_type(name):
    type = services.get_type(name)
    return services.update_type(type)


@app.route('/api/types/<str:name>', methods=['DELETE', ])
def delete_type(name: str):
    type = services.delete_type(name)
    return Response(status=204)


@app.route('/api/types/<str:name>/export/xsd', methods=['GET', ])
def export_type(name: str):
    return {

    }
