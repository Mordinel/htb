import traceback

from flask_restplus import Api
from craft_api import settings

api = Api(version='1.0', title='Craft API',
          description='An API for IPA\'s')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
