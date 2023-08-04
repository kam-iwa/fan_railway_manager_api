from io import BytesIO
from flask import Blueprint, jsonify, request, render_template, send_file
from flasgger import swag_from
from peewee import fn
import json

from models.routes import Route
from models.stations import Station
from models.stops import Stop
from routings.api import route_mod

@route_mod.route('/api/routes', methods=['GET'])
@swag_from('docs/routes.get.yml')
def routes_get():
    routes = Route.select()
    return jsonify([{"id": route.id, "number": route.number, "name": route.name} for route in routes])

@route_mod.route('/api/routes/<int:route_id>', methods=['GET'])
@swag_from('docs/routes.route_id.get.yml')
def routes_route_id_get(route_id: int):
    route = Route.get_or_none(Route.id == route_id)
    if route is None:
        return jsonify({'error': 'Route not found.'})
    
    result = {
        "id": route.id,
        "name": route.name,
        "number": route.number,
        "stops": []
    }
    stops = Stop.select().where(Stop.route == route.id).order_by(Stop.departure_time)
    for stop in stops:
        result["stops"].append({"station": stop.station.name, "arrival": str(stop.arrival_time), "departure": str(stop.departure_time)})
    
    return jsonify({'data': result})

@route_mod.route('/api/routes', methods=['POST'])
@swag_from('docs/routes.post.yml')
def routes_create():

    data = request.get_json()["data"]
    route = Route.create(**data)

    stops = data["stops"]
    for stop in stops:
        print(stop)
        stop["route"] = route.id
        station = Station.get_or_none(fn.lower(Station.name) == fn.lower(fn.trim(station.name)))
        if station is None:
            return jsonify({'error': 'Station not found.'})
        
        stop["station"] = station.id
        Stop.create(**stop)

    return jsonify({'data': route.id}), 201


@route_mod.route('/api/routes/<int:route_id>', methods=["PUT"])
def route_edit(route_id: int):
    route = Route.get_or_none(id == route_id)
    if route is None:
        return jsonify({'error': 'Route not found.'})
    
    data = request.get_json()["data"]
    route = Route.update(**data)

    return jsonify({}), 200


@route_mod.route('/api/routes/<int:route_id>', methods=["DELETE"])
def route_delete(route_id: int):
    route = Route.get_or_none(id == route_id)
    if route is None:
        return jsonify({'error': 'route not found.'})
    
    Route.delete().where(route.id == route_id)
    return jsonify({}), 204

