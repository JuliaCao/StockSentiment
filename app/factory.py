import os
from flask import Flask, g
from werkzeug.utils import find_modules, import_string
import sys
sys.path.append("/Users/Miaomiao0808/stockSentiment/app")
from blueprints.app import init_db


def create_app(config=None):
    app = Flask('stockSentiment')

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'stockSentiment.db'),
        DEBUG=True,
        SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
        USERNAME='admin',
        PASSWORD='default'
    ))
    app.config.update(config or {})
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    register_blueprints(app)
    register_cli(app)
    register_teardowns(app)

    return app


def register_blueprints(app):
    """Register all blueprint modules
    """
    for name in find_modules('app.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def register_cli(app):
    @app.cli.command('initdb')
    def initdb_command():
        """Creates the database tables."""
        init_db()
        print('Initialized the database.')


def register_teardowns(app):
    @app.teardown_appcontext
    def close_db(error):
        """Closes the database again at the end of the request."""
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()