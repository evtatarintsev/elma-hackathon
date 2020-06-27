import io

import click
from flask import Flask
from flask import request, make_response, send_file
from flask.cli import with_appcontext
from marshmallow import ValidationError

from . import repository, services
from .schemas import TypeSchema
from .xsd import to_xsd

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
        saved_type = services.create_type(new_type)
    except ValidationError as err:
        return err.messages, 400

    return TypeSchema().dump(saved_type)


@app.route('/api/types/<string:name>/update', methods=['PUT', ])
def update_type(name):
    try:
        draft_type = TypeSchema().load(request.get_json())
        saved_type = services.update_type(name, draft_type)
    except ValidationError as err:
        return err.messages, 400

    return TypeSchema().dump(saved_type)


@app.route('/api/types/<string:name>/delete', methods=['DELETE', ])
def delete_type(name: str):
    try:
        services.delete_type(name)
    except ValidationError as err:
        return err.messages, 400
    return {}, 204


@app.route('/api/types/<string:name>/export/xsd', methods=['GET', ])
def export_type(name: str):
    type = services.get_type(name)
    response = make_response(to_xsd(type))
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/api/types/<string:name>/export/xsd/save', methods=['GET', ])
def export_save_type(name: str):
    type = services.get_type(name)
    xsd = io.BytesIO(to_xsd(type).encode())
    return send_file(xsd, as_attachment=True, attachment_filename='type.xsd')


@app.teardown_appcontext
def shutdown_session(exception=None):
    repository.db_session.remove()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    repository.init_db()
    click.echo('Initialized the database.')


app.cli.add_command(init_db_command)
