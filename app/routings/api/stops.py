from flask import Blueprint, jsonify, request

from models.stations import Station
from models.stops import Stop
from models.routes import Route
from routings.api import stop_mod


@stop_mod.route('/stops', methods=['GET'])
def stops_get():
    stops = Stop.select()
    return jsonify([{"id": stop.id} for stop in stops])


@stop_mod.route('/stops', methods=['POST'])
def stops_create():
    data = request.get_json()["data"]
    stop = Stop.create(**data)

    return jsonify({'data': stop.id}), 201


@stop_mod.route('/stops/<int:stop_id>', methods=["PUT"])
def stop_edit(stop_id: int):
    stop = Stop.get_or_none(id == stop_id)
    if stop is None:
        return jsonify({'error': 'Stop not found.'})
    
    data = request.get_json()["data"]
    stop = Stop.update(**data)

    return jsonify({}), 200


@stop_mod.route('/stops/<int:stop_id>', methods=["DELETE"])
def stop_delete(stop_id: int):
    stop = Stop.get_or_none(id == stop_id)
    if stop is None:
        return jsonify({'error': 'stop not found.'})
    
    Stop.delete().where(stop.id == stop_id)
    return jsonify({}), 204