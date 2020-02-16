import os
from flask import Flask, Blueprint
from werkzeug.contrib.fixers import ProxyFix
from craft_api import settings
from craft_api.api.auth.endpoints.auth import ns as craft_auth_namespace
from craft_api.api.brew.endpoints.brew import ns as craft_brew_namespace
from craft_api.api.restplus import api
from craft_api.database import db

app = Flask(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s' % ( settings.MYSQL_DATABASE_USER, settings.MYSQL_DATABASE_PASSWORD, settings.MYSQL_DATABASE_HOST, settings.MYSQL_DATABASE_DB)
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(craft_auth_namespace)
    api.add_namespace(craft_brew_namespace)
    flask_app.register_blueprint(blueprint)
    flask_app.wsgi_app = ProxyFix(app.wsgi_app)

    db.init_app(flask_app)

def main():
    initialize_app(app)
    app.run(host='0.0.0.0', port=8888, debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
