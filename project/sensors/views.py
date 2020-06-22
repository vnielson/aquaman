from flask import render_template, Blueprint, url_for, redirect, request, jsonify
from project import db
from project.sensors import moisturemeter
from project.models import Sensors
from project.models import SensorReadings
from project.sensors.forms import AddSensorForm, DeleteSensorForm

sensor_data = Blueprint('sensor_data', __name__)


def load_data():

    sensor_data = []
    sensors = Sensors.query.all()
    for s in sensors:
        next_sensor = s.__dict__
        del next_sensor["_sa_instance_state"]
        sensor_data.append(next_sensor)

    print("Sensor Data... ")
    print(sensor_data)
    return sensor_data

@sensor_data.route('/sensors/', methods=['GET'])
def get_data():
    print("IN getData for sensors")
    return jsonify(load_data())



@sensor_data.route('/sensors/readings/', methods=['GET'])
def get_sensor_readings():

    readings = SensorReadings.query.all()

    sensor_readings = []

    for s in readings:
        next_reading = s.__dict__
        del next_reading["_sa_instance_state"]
        sensor_readings.append(next_reading)

    print("Sensor Readings:")
    print(sensor_readings)

    return jsonify(sensor_readings)


@sensor_data.route('/sensors/', methods=['POST',])
def insert_data():
    print("Insert Sensor Request...")
    new_sensor_data = request.json
    print(new_sensor_data)

    # Create the New Sensor

    new_sensor = Sensors(
        configuration=new_sensor_data["configuration"],
        crop_id=new_sensor_data["crop_id"],
        valve_id = new_sensor_data["valve_id"],
        bcm_pin=new_sensor_data["bcm_pin"]
    )


    # def __init__(self, first_name, last_name, login_id, judging_event_id, school_id):

    db.session.add(new_sensor)
    db.session.commit()



    ret_sensor = {
        "sensor_id": new_sensor.sensor_id,
        "configuration": new_sensor.configuration,
        "crop_id": new_sensor.crop_id,
        "valve_id": new_sensor.valve_id,
        "bcm_pin": new_sensor.bcm_pin
    }

    return jsonify(ret_sensor)
    # return jsonify(success=True)




@sensor_data.route('/sensors/<int:sensor_id>', methods=['PUT',])
def update_sensor(sensor_id):

    print("UPDATE SENSOR:")
    #Find item to update
    jsonrequest = request.json
    print("json request")
    print(jsonrequest)

    sensor = db.session.query(Sensors).get(jsonrequest["sensor_id"]);
    print("Sensor to be updated:")
    print(sensor)

    update = {
        "configuration" : jsonrequest["configuration"],
        "crop_id": jsonrequest["crop_id"],
        "valve_id": jsonrequest["valve_id"],
        "bcm_pin": jsonrequest["bcm_pin"]
    }

    print(update)

    db.session.query(Sensors).filter_by(sensor_id=jsonrequest["sensor_id"]).update(update)
    db.session.commit();


    return jsonify(request.json)
    # return jsonify(success=True)


@sensor_data.route('/sensors/<int:sensor_id>', methods=['DELETE',])
def delete_sensor(sensor_id):

    sensor = db.session.query(Sensors).get(sensor_id);

    del_school_return = db.session.delete(sensor)
    print("Return value  ", del_school_return)

    db.session.commit()

    return jsonify(success=True)


@sensor_data.route('/sensors/get_reading/<int:sensor_id>', methods=['GET'])
def get_sensor_reading(sensor_id):
    print("IN getreading for sensor:")
    print(sensor_id)

    Sensor = Sensors.query.get(sensor_id)
    print("Next Sensor: {} {} {}".format(Sensor.sensor_id, Sensor.crop, Sensor.bcm_pin))
    sensor = moisturemeter.MoistureMeter(Sensor.sensor_id, Sensor.bcm_pin)
    print("Sensor: ")
    print(sensor)
    sensor_reading_data = sensor.get_kpa_value()

    print(sensor_reading_data)
    return jsonify(sensor_reading_data)

