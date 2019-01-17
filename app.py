from flask import Blueprint
from flask_restful import Api
from resources.Location import LocationResource
from resources.Value import ValueResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes

api.add_resource(LocationResource, '/Locations',
                 '/Location/<int:item_id>', endpoint='item_id')
api.add_resource(ValueResource, '/Values',
                 '/Values/<int:loc_id>', endpoint='loc_id')
