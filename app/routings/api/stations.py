from io import StringIO
from flask import Blueprint, jsonify, request, render_template, make_response
from flask.helpers import send_file
from flasgger import swag_from
from peewee import fn
import csv
from utils.stations import get_station_routes

from models.routes import Route
from models.stations import Station
from models.stops import Stop

station_mod = Blueprint('station', __name__)


@station_mod.route('/api/stations', methods=['GET'])
@swag_from('docs/stations.get.yml')
def stations_get():
    stations = Station.select()
    return jsonify([{"name":station.name, "lat": station.lat, "lon": station.lon, "is_stop": station.is_stop} for station in stations])

@station_mod.route('/api/stations/<station_name>', methods=['GET'])
@swag_from('docs/stations.station_name.get.yml')
def stations_station_get(station_name: str):
    station = Station.get_or_none(fn.lower(Station.name) == station_name.strip().lower())
    if station is None:
        return jsonify({'error': 'Station not found.'})
    
    return jsonify({"name":station.name, "lat": station.lat, "lon": station.lon, "is_stop": station.is_stop})


@station_mod.route('/api/stations', methods=['POST'])
@swag_from('docs/stations.post.yml')
def stations_create():
    data = request.get_json()["data"]
    station = Station.create(**data)

    return jsonify({'data': station.id}), 201


@station_mod.route('/api/stations/<int:station_id>', methods=["PUT"])
#@swag_from('docs/stations.station_id.put.yml')
def stations_edit(station_id: int):
    station = Station.get_or_none(id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})
    
    data = request.get_json()["data"]
    station = Station.update(**data)

    return jsonify({}), 200


@station_mod.route('/api/stations/<int:station_id>', methods=["DELETE"])
#@swag_from('docs/stations.station_id.delete.yml')
def stations_delete(station_id: int):
    station = Station.get_or_none(id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})
    
    Station.delete().where(Station.id == station_id)
    return jsonify({}), 204


@station_mod.route('/api/stations/<station_name>/routes', methods=['GET'])
@swag_from('docs/stations.station_name.routes.get.yml')
def stations_routes_get(station_name: str):
    if(station := Station.get_or_none(Station.name.lower == station_name.lower)) is None:
        return jsonify({'error': 'Station not found.'})
    
    result = get_station_routes(station)

    return jsonify(result)





@station_mod.route('/api/stations/from_csv', methods=['POST'])
@swag_from('docs/stations.from_csv.post.yml')
def stations_from_csv():
    file = request.files['file']
    file_string = file.read()
    file_readed = StringIO(file_string.decode())
    csv_data = csv.reader(file_readed)
    for row in csv_data:
        if row[3] == 'false':
            is_station = False
        else:
            is_station = True
        Station.create(
            name=row[0],
            lat=row[1],
            lon=row[2],
            station=is_station
        )

    return jsonify({}), 200
    