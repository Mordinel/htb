from flask_restplus import fields
from craft_api.api.restplus import api

beer_entry = api.model('A craft brew', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of the beverage'),
    'brewer': fields.String(required=True, description='Name of brewery'),
    'name': fields.String(required=True, description='Name of the brew'),
    'style': fields.String(required=True, description='Style of the brew'),
    'abv': fields.String(required=True, description='ABV of the brew')
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_beer_entries = api.inherit('A page of brews', pagination, {
    'items': fields.List(fields.Nested(beer_entry))
})