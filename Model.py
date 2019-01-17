from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import datetime
ma = Marshmallow()
db = SQLAlchemy()


class Location(db.Model):
    __tablename__ = 'locationtest'
    __table_args__ = {'schema': 'agro_data'}
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    coordinates = Column(JSON, nullable=False)
    poly_id = Column(String(250), nullable=True)

    def __init__(self, name, coordinates, poly_id=None):
        self.name = name
        self.poly_id = poly_id
        self.coordinates = coordinates


class LocationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    coordinates = fields.List(fields.List(
        fields.List(fields.Float(required=True))))
    poly_id = fields.String(required=False)



class Type(db.Model):
    __tablename__ = 'types'
    __table_args__ = {'schema': 'agro_data'}
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    unit = Column(String(250), nullable=False)


class Value(db.Model):
    __tablename__ = 'valuestest'
    __table_args__ = {'schema': 'agro_data'}
    id = Column(Integer, primary_key=True)
    timestamp = Column(String(250), nullable=False)
    typeid = Column(Float, ForeignKey(Type.id))
    value = Column(Float, nullable=True)
    forecasted = Column(String(250), nullable=False)
    locationid = Column(Integer, db.ForeignKey(Location.id), nullable=True)
    location = db.relationship(Location, backref=db.backref('valuestest'))

    def __init__(self, timestamp, typeid, value, forecasted, locationid):
        self.timestamp = timestamp
        self.typeid = typeid
        self.value = value
        self.forecasted = forecasted
        self.locationid = locationid


class ValueSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    dt = fields.Integer(required=True)
    typeid = fields.Float(required=False)
    value = fields.String(required=False)
    forecasted = fields.String(required=False)
    locationid = fields.Integer(required=False)
