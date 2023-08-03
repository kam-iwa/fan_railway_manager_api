from peewee import Model, AutoField, TextField, ForeignKeyField, BooleanField, DateField

from app import db

class Route(Model):

    class Meta:
        database = db

    id = AutoField(primary_key=True)
    number = TextField()
    name = TextField()
    fast = BooleanField(default=False)
    parent_route = ForeignKeyField('self', null=True, default=None)

    # DNI KURSOWANIA
    date_start = DateField(null=True)
    date_end = DateField(null=True)

    date_monday = BooleanField(null=True)
    date_tuesday = BooleanField(null=True)
    date_wednesday = BooleanField(null=True)
    date_thursday = BooleanField(null=True)
    date_friday = BooleanField(null=True)
    date_saturday = BooleanField(null=True)
    date_sunday = BooleanField(null=True)

    # INFORMACJE
    info_first_class = BooleanField(null=True)
    info_second_class = BooleanField(null=True)
    info_reservation = BooleanField(null=True)
    info_minibar = BooleanField(null=True)
    info_restaurant = BooleanField(null=True)
    info_sleeping = BooleanField(null=True)
    info_couchette = BooleanField(null=True)
    info_bicycles = BooleanField(null=True)