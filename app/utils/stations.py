from models.routes import Route
from models.stations import Station
from models.stops import Stop


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