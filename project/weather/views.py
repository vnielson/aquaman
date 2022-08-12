import datetime
from flask import render_template, Blueprint, url_for, redirect, jsonify, request
from project import db
from project.models import WeatherData
from project.weather import bme280_sensor

from project.core.aqualogger import weatherlog

weather = Blueprint('weather', __name__)



@weather.route('/weather/', methods=['GET'])
def get_data():
    weatherlog.debug("IN getData for weather")
    return render_template('weather.html')

@weather.route('/weather/current', methods=['GET'])
def get_current_weather():
    current_weather = get_current_weather_data()
    return jsonify(current_weather)


@weather.route('/weather/readings', methods=['GET'])
def get_weather_readings():
    weatherlog.debug("Weather Readings:")
    # user = request.args.get('user')
    # weatherlog.debug(request.args)
    # sort_order = request.args.get('sort_order')
    # if sort_order is None:
    #     sort_order = ''

    # weatherlog.debug("Sort Order: " + sort_order)

    days_to_fetch = request.args.get('days')
    if days_to_fetch is None:
        readings = WeatherData.query.order_by(WeatherData.timestamp)
    else:
        filter_after = datetime.datetime.today() - datetime.timedelta(days=int(days_to_fetch))
        readings = WeatherData.query.filter(WeatherData.timestamp >= filter_after).order_by(WeatherData.timestamp)

    # payments = Payment.query.filter(Payment.due_date >= filter_after).all()

    # jsonrequest = request.json
    # weatherlog.debug("json request")
    # weatherlog.debug(jsonrequest)
    #
    # if jsonrequest:
    #     sort_order = jsonrequest["sort_order"]


    weather_readings = []

    first = True

    # sensors = Sensors.query.all()
    # sensor_data = {}
    # for s in sensors:
    #     sensor_data[s.sensor_id] = s.sensor_name
    #
    # weatherlog.debug(sensor_data)

    for r in readings:
        next_reading = r.__dict__
        del next_reading["_sa_instance_state"]
        weatherlog.debug(next_reading)
        weather_readings.append(next_reading)

    # weatherlog.debug("Sensor Readings:")
    # count = 0
    # for reading in weather_readings:
    #     weatherlog.debug(reading)
    #     count += 1
    #     if count > 50:
    #         break

    jsonData = jsonify(weather_readings)
    weatherlog.debug(jsonData)

    return jsonify(weather_readings)


def get_current_weather_data():
    bme280 = bme280_sensor.bme280_sensor()
    current_weather = bme280.get_weather_reading()
    return current_weather

def do_weather_reading():

    bme280 = bme280_sensor.bme280_sensor()
    current_weather = bme280.get_weather_reading()

    weatherlog.info("Current Weather Data:")
    weatherlog.info(current_weather)

    new_reading = WeatherData(current_weather)
    db.session.add(new_reading)
    db.session.commit()




