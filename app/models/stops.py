from peewee import Model, AutoField, ForeignKeyField, TimeField

from models.stations import Station
from models.routes import Route
from app import db


class Stop(Model):
    id = AutoField(primary_key=True)
    route = ForeignKeyField(Route, column_name='route')
    station = ForeignKeyField(Station, column_name='station')
    arrival_time = TimeField()
    departure_time = TimeField()

    #platform = TextField(null=True)
    #track = TextField(null=True)

    class Meta:
        database = db