from flask import jsonify, render_template
from routings.api import station_mod
from models.stations import Station
from utils.stations import get_station_routes


@station_mod.route('/web/stations/<station_name>/timetable', methods=["GET"])
def stations_timetable(station_name: str):
    if(station := Station.get_or_none(Station.name == station_name)) is None:
        return jsonify({'error': 'Station not found.'})
    
    result = get_station_routes(station)
    
    return render_template('departures.html',
                           station_name=station_name,
                           routes=result['data']['routes'])