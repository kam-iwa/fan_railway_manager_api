from io import BytesIO
from flask import Blueprint, jsonify, request, render_template, send_file
from flasgger import swag_from
import json

from models.routes import Route
from models.stations import Station
from models.stops import Stop

route_mod = Blueprint('route', __name__)


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
    args = request.args
    create_stops = args.get('create_stops')

    data = request.get_json()["data"]
    route = Route.create(**data)

    stops = data["stops"]
    for stop in stops:
        print(stop)
        stop["route"] = route.id
        if create_stops is None or json.loads(create_stops) == False:
            station = Station.get(Station.name == stop["station"])
        else:
            station = Station.get_or_create(Station.name == stop["station"])
        
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

