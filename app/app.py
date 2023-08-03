from flask import Flask
from flasgger import Swagger
from peewee import PostgresqlDatabase

# Create the Flask app
app = Flask(__name__)

# Create the database connection
db = PostgresqlDatabase(
    database='trains',
    user='docker',
    password='docker',
    host='db',
    port=5432
)

# Create the Swagger instance
swagger = Swagger(app)

# Register the blueprints for each route
def register_blueprints():
    from routings.api.stations import station_mod
    from routings.api.routes import route_mod
    from routings.api.stops import stop_mod

    app.register_blueprint(station_mod)
    app.register_blueprint(route_mod)
    app.register_blueprint(stop_mod)


# Initialize the database
def create_tables():
    from models.routes import Route
    from models.stations import Station
    from models.stops import Stop
    with db:
        db.create_tables([Station, Route, Stop])


if __name__ == '__main__':
    register_blueprints()
    create_tables()
    app.run(host='0.0.0.0', debug=True)