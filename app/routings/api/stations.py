from io import StringIO
from flask import Blueprint, jsonify, request, render_template, make_response
from flask.helpers import send_file
from flasgger import swag_from
from peewee import fn
import csv

from models.routes import Route
from models.stations import Station
from models.stops import Stop

station_mod = Blueprint('station', __name__)


@station_mod.route('/stations', methods=['GET'])
@swag_from('docs/stations.get.yml')
def stations_get():
    stations = Station.select()
    return jsonify([{"name":station.name, "lat": station.lat, "lon": station.lon} for station in stations])


@station_mod.route('/stations', methods=['POST'])
@swag_from('docs/stations.post.yml')
def stations_create():
    data = request.get_json()["data"]
    station = Station.create(**data)

    return jsonify({'data': station.id}), 201

@station_mod.route('/stations/from_csv', methods=['POST'])
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


@station_mod.route('/stations/<int:station_id>', methods=["PUT"])
#@swag_from('docs/stations.station_id.put.yml')
def stations_edit(station_id: int):
    station = Station.get_or_none(id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})
    
    data = request.get_json()["data"]
    station = Station.update(**data)

    return jsonify({}), 200


@station_mod.route('/stations/<int:station_id>', methods=["DELETE"])
#@swag_from('docs/stations.station_id.delete.yml')
def stations_delete(station_id: int):
    station = Station.get_or_none(id == station_id)
    if station is None:
        return jsonify({'error': 'Station not found.'})
    
    Station.delete().where(Station.id == station_id)
    return jsonify({}), 204


@station_mod.route('/stations/<station_name>/routes', methods=['GET'])
@swag_from('docs/stations.station_name.routes.get.yml')
def stations_routes_get(station_name: str):
    if(station := Station.get_or_none(Station.name == station_name)) is None:
        return jsonify({'error': 'Station not found.'})
    
    result = get_station_routes(station)

    return jsonify(result)


@station_mod.route('/stations/<station_name>/timetable', methods=["GET"])
@swag_from('docs/stations.station_name.timetable.get.yml')
def stations_timetable(station_name: str):
    if(station := Station.get_or_none(Station.name == station_name)) is None:
        return jsonify({'error': 'Station not found.'})
    
    result = get_station_routes(station)
    
    return render_template('departures.html',
                           station_name=station_name,
                           routes=result['data']['routes'])


def get_station_routes(station: Station):
    station_id = station.id

    routes = Stop.select(
            Stop.arrival_time.cast('text'), Stop.departure_time.cast('text'), Route
        ).order_by(
            Stop.arrival_time
        ).join(
            Route, on=(Route.id == Stop.route)
        ).join(
            Station, on=(Station.id == Stop.station)
        ).where(
            Stop.station == station_id
        ).order_by(
            Stop.departure_time
        ).dicts()
    
    result = {"data": {
        "station": station.name,
        "routes": []
    }}
    for route in routes:
        query = Stop.select(
                Station.name, Stop.arrival_time.cast('text')
            ).where( 
                Stop.route == route['id']
            ).join(
                Station, on=(Station.id == Stop.station)
            ).where(
                Stop.arrival_time > route["arrival_time"]
            ).order_by(
                Stop.arrival_time
            )
        
        q, param = query.sql()
        print(q, param)
        
        route_data = {
            "train_name": route['name'],
            "train_number": route['number'],
            "departure_time": route['departure_time'][:-3],
            "intermediate_stops": [],
            "destination": [],
            "fast": route['fast'],
            "info_first_class": route["info_first_class"],
            "info_second_class": route["info_second_class"],
            "info_reservation": route["info_reservation"],
            "info_reservation_compulsory": route["info_reservation_compulsory"],
            "info_minibar": route['info_minibar'],
            "info_restaurant": route['info_restaurant'],
            "info_sleeping": route['info_sleeping'],
            "info_couchette": route['info_couchette'],
            "info_bicycles": route['info_bicycles']
        }
        for row in query.dicts():
            route_data['intermediate_stops'].append({"station": row['name'], "arrival_time": row['arrival_time'][:-3]})

        try:
            route_data['destination'] = route_data['intermediate_stops'][-1]
            route_data['intermediate_stops'].pop()
            result['data']['routes'].append(route_data)
        except IndexError:
            route_data['destination'] = []

    return result
    