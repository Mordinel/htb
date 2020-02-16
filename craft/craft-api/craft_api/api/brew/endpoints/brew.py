

from flask import request, jsonify, make_response
from flask_restplus import Resource
from craft_api.api.restplus import api
from craft_api.api.auth.endpoints import auth
from craft_api.api.brew.operations import create_brew, update_brew, delete_brew
from craft_api.api.brew.serializers import beer_entry, page_of_beer_entries
from craft_api.api.brew.parsers import pagination_arguments
from craft_api.database.models import Brew
from functools import wraps
import datetime 

ns = api.namespace('brew/', description='Operations related to beer.')


@ns.route('/')
class BrewCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_beer_entries)
    def get(self):
        """
        Returns list of brews.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        brews_query = Brew.query
        brews_page = brews_query.paginate(page, per_page, error_out=False)

        return brews_page

    @auth.auth_required
    @api.expect(beer_entry)
    def post(self):
        """
        Creates a new brew entry.
        """

        # make sure the ABV value is sane.
        if eval('%s > 1' % request.json['abv']):
            return "ABV must be a decimal value less than 1.0", 400
        else:
            create_brew(request.json)
            return None, 201

@ns.route('/<int:id>')
@api.response(404, 'Brew not found.')
class BrewItem(Resource):

    @api.marshal_with(beer_entry)
    def get(self, id):
        """
        Returns brew data.
        """
        return Brew.query.filter(Brew.id == id).one()

    @auth.auth_required
    @api.expect(beer_entry)
    @api.response(204, 'Brew successfully updated.')
    def put(self, id):
        """
        Updates a brew.
        """
        data = request.json
        update_brew(id, data)
        return None, 204

    @auth.auth_required
    @api.response(204, 'Brew successfully deleted.')
    def delete(self, id):
        """
        Deletes a brew.
        """
        delete_brew(id)
        return None, 204