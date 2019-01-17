from flask import request
from flask_restful import Resource
from Model import db, Location, LocationSchema, Value, ValueSchema,Type
from werkzeug.exceptions import BadRequest
from sqlalchemy.orm.exc import NoResultFound,  MultipleResultsFound
from sqlalchemy.exc import IntegrityError

values_schema = ValueSchema(many=True)
value_schema = ValueSchema()

class ValueResource(Resource):
    def post(self, loc_id=None):
        try:
            json_data = request.get_json(force=True)
        except BadRequest:
            return {'message': 'No input data provided or no JSON format'}, 400
        # Validate and deserialize input
        data, errors = value_schema.load(json_data)
        if errors:
            return errors, 422
        try:
            location = Location.query.filter_by(id=loc_id).one()
            print(location.id)
        except NoResultFound:
            return {'message': 'There is no Location with id = ' + str(loc_id)}, 400
        VALUE_TYPE={
            'temp': [json_data['main']['temp'], 1],
            'pressure': [json_data['main']['pressure'], 2],
            'humidity': [json_data['main']['humidity'], 3],
            'windspeed': [json_data['wind']['speed'], 4],
            'winddirection': [json_data['wind']['deg'], 5],
            'cloudiness': [json_data['clouds']['all'], 6],
        }
        for key, value in VALUE_TYPE.items():
            db.session.rollback()
            val = Value(
                timestamp=json_data['dt'],
                typeid=value[1],
                value=value[0],
                forecasted='False',
                locationid=location.id
            )
            try:
                db.session.add(val)
                db.session.commit()
            except IntegrityError:
                continue

        # result = value_schema.dump(val).data
        return {"status": 'success'}, 204
