from peewee import Model, AutoField, ForeignKeyField, TimeField, IntegerField

from models.stations import Station
from models.routes import Route
from app import db


class Stop(Model):
    id = AutoField(primary_key=True)
    route = ForeignKeyField(Route, column_name='route')
    station = ForeignKeyField(Station, column_name='station')
    arrival_time = TimeField()
    arrival_day = IntegerField(default=0)
    departure_time = TimeField()
    departure_day = IntegerField(default=0)

    class Meta:
        database = db