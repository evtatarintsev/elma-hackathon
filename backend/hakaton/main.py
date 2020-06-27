from flask import Flask
app = Flask(__name__)


@app.route('/api/types', methods=['GET', ])
def types():
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
