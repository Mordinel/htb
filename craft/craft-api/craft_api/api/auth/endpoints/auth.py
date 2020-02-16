

from flask import request, jsonify, make_response
from flask_restplus import Resource
from craft_api import settings
from craft_api.api.restplus import api
from functools import wraps
from craft_api.database.models import User
import datetime 
import jwt

ns = api.namespace('auth/', description='Operations related to authentication')

secret = settings.CRAFT_API_SECRET

authorizations = {
    'apikey' : { 

        'type' : 'apiKey',
        'in' : 'header',
        'name': 'X-Craft-Api-Token'
    }
}

def auth_login():

    auth = request.authorization

    try: 
        auth_results = User.query.filter(User.username == auth.username, User.password == auth.password).one()
    except: 
        auth_results = ''
    
    if type(auth_results) is User:
        
        token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, secret)
        
        return jsonify({'token' : token.decode('UTF-8')})
    
    return make_response('Authentication failed', 401, {'WWW-Authenticate' : 'Basic realm="Craft API Login"'})

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        if 'X-Craft-Api-Token' in request.headers:
            token = request.headers['X-Craft-Api-Token']
        
        try:
            token_decoded = jwt.decode(token, secret)
        except:
            return {'message' : 'Invalid token or no token found.'}, 403

        return f(*args, **kwargs)

    return decorated

@ns.route('/login')
class AuthCollection(Resource):
    def get(self):
        """
        Create an authentication token provided valid username and password.
        """
        token = auth_login()
        return token


@ns.route('/check')
class AuthCollection(Resource):
    @auth_required
    def get(self):
        """
        Checks validity of an authorization token
        """
        return jsonify({'message' : 'Token is valid!'})