from peewee import Model, AutoField, TextField, DecimalField, BooleanField

from app import db

class Station(Model):
    id = AutoField(primary_key=True)
    name = TextField(unique=True)
    lat = DecimalField(null=True)
    lon = DecimalField(null=True)

    is_stop = BooleanField(default=False)

    class Meta:
        database = db