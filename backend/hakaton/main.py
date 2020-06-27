import click

from flask import Flask
from flask import request, Response
from flask.cli import with_appcontext

from . import repository, services


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


@app.route('/api/types/<string:name>', methods=['PUT', ])
def update_type(name):
    type = services.get_type(name)
    return services.update_type(type)


@app.route('/api/types/<string:name>', methods=['DELETE', ])
def delete_type(name: str):
    type = services.delete_type(name)
    return Response(status=204)


@app.route('/api/types/<string:name>/export/xsd', methods=['GET', ])
def export_type(name: str):
    return {

    }


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
