from io import BytesIO
from flask import Blueprint, jsonify, request, render_template, send_file
from flasgger import swag_from
import json

from ..api.routes import route_mod
from models.routes import Route
from models.stations import Station
from models.stops import Stop

@route_mod.route('/routes/<int:route_id>/table', methods=["GET"])
def route_route_id_table(route_id: int):
    route = Route.get_or_none(Route.id == route_id)
    if route is None:
        return jsonify({'error': 'Route not found.'})
    
    result = {
        "id": route.id,
        "name": route.name,
        "number": route.number,
        "fast": route.fast,
        "stops": []
    }
    stops = Stop.select().where(Stop.route == route.id).order_by(Stop.departure_time)
    for stop in stops:
        result["stops"].append({"station": stop.station.name, "arrival": str(stop.arrival_time), "departure": str(stop.departure_time)})

    return render_template('route.html', number=result['number'], name=result['name'], stops=result["stops"], fast=result['fast'])

@route_mod.route('/routes/add_route', methods=["GET", "POST"])
def route_add():
    if request.method == "POST":
        print(request.form)
        
        route = {
            "name": request.form.get('train_name'),
            "number": request.form.get('train_number'),
            "fast": bool(request.form.get('train_fast')),
            "stops": []
        }

        route_len = 0
        for i in range(0, 32):
            station = request.form.get(f'train_stop_{i}_station')
            arrival_time = request.form.get(f'train_stop_{i}_arrival')
            departure_time = request.form.get(f'train_stop_{i}_departure')
            
            if station == '' or arrival_time == '' or departure_time == '':
                continue
            else:
                route["stops"].append(
                    {
                        "station": station,
                        "arrival_time": arrival_time,
                        "departure_time": departure_time
                    }
                )
                route_len += 1

        print(route)
        if route_len > 1:
            create_route(route)


        # for stop in request.form.get('stops').replace('\r','').split('\n'):
        #     stop_data = stop.split(',')
        #     print(stop_data)
        #     route["stops"].append(
        #         {
        #             "station": stop_data[0],
        #             "arrival_time": stop_data[1],
        #             "departure_time": stop_data[2]
        #         }
        #     )
        # create_route(route)
        # print(route)

    return render_template('route_add.html')

def create_route(data: dict):
    route = Route.create(**data)

    stops = data["stops"]
    for stop in stops:
        print(stop)
        stop["route"] = route.id
        station = Station.get(Station.name == stop["station"])
        
        stop["station"] = station.id
        Stop.create(**stop)
        