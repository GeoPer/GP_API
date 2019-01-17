from flask import request
from flask_restful import Resource
from Model import db, Location, LocationSchema
from werkzeug.exceptions import BadRequest
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

locations_schema = LocationSchema(many=True)
location_schema = LocationSchema()


class LocationResource(Resource):

    def get(self, item_id=None):
        if (item_id == None):
            locations_in_db = Location.query.all()
            locations_data = locations_schema.dump(locations_in_db).data
            if locations_data:
                return {'status': 'success', 'data': locations_data}, 200
            else:
                return {'message': 'There are no Locations on our DB'}, 404
        else:
            location_in_db = Location.query.filter_by(id=item_id)
            location_data = locations_schema.dump(location_in_db).data
            if location_data:
                return {'status': 'success', 'data': location_data}, 200
            else:
                return {'message': 'There is no entry with id:' + str(item_id)}, 404

    def post(self):
        try:
            json_data = request.get_json(force=True)
        except:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = location_schema.load(json_data)
        if errors:
            return errors, 422
        location_in_db = Location.query.filter_by(name=data['name']).first()
        if location_in_db:
            return {'message': 'Location already exists'}, 400
        if "id" in json_data:
            location = Location(
                name=json_data['name'],
                coordinates=json_data['geo_json']['geometry']['coordinates'],
                poly_id=json_data['id']
            )
        else:
            location = Location(
                name=json_data['name'],
                coordinates=json_data['geo_json']['geometry']['coordinates']
            )
        db.session.add(location)
        db.session.commit()
        result = location_schema.dump(location).data
        return {"status": 'success', 'data': result}, 201

    def delete(self, item_id=None):
        if item_id:
            location_in_db = Location.query.filter_by(id=item_id).all()
            if location_in_db:
                location_data = locations_schema.dump(location_in_db).data
                Location.query.filter_by(id=item_id).delete()
                db.session.commit()
                return {'status': 'success', 'data': location_data}, 200
            else:
                return {'message': 'There is no entry with id: ' + str(item_id)}, 404

    def patch(self, item_id=None):
        try:
            json_data = request.get_json(force=True)
        except BadRequest:
            return {'message': 'No input data provided or no JSON format'}, 400
        # Validate and deserialize input
        data, errors = location_schema.load(json_data)
        if errors:
            return errors, 422
        try:
            location_for_update = Location.query.filter_by(id=item_id).one()
        except NoResultFound:
            return {'message': 'There is no Location with id = ' + str(item_id)}, 400
        except MultipleResultsFound:
            raise

        location_for_update.coordinates = json_data['geo_json']['geometry']['coordinates']
        db.session.commit()
        location_new_data = location_schema.dump(location_for_update).data
        return {'status': 'success', 'data': location_new_data}, 200

