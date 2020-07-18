import datetime
from flask import render_template, Blueprint, url_for, redirect, request, jsonify
from project import db
from project.sensors import moisturemeter
from project.models import Sensors
from project.models import SensorReadings
from project.sensors.forms import AddSensorForm, DeleteSensorForm

sensor_data = Blueprint('sensor_data', __name__)


def load_data():

    print("Load Data:")

    sensor_data = []
    sensors = Sensors.query.all()
    for s in sensors:
        next_sensor = s.__dict__
        v_data = s.valves.__dict__
        c_data = s.crops.__dict__
        del next_sensor["_sa_instance_state"]
        print(next_sensor)
        row_data = {}
        row_data["sensor_id"] = next_sensor["sensor_id"]
        row_data["sensor_name"] = next_sensor["sensor_name"]
        row_data["valve_id"] = next_sensor["valve_id"]
        row_data["bcm_pin"] = next_sensor["bcm_pin"]
        row_data["configuration"] = next_sensor["configuration"]
        row_data["crop_id"] = next_sensor["crop_id"]
        row_data["valve_name"] = v_data["valve_name"]
        row_data["crop_name"] = c_data["crop_name"]
        sensor_data.append(row_data)

    # print("Sensor Data... ")
    # print(sensor_data)
    return sensor_data

@sensor_data.route('/sensors/', methods=['GET'])
def get_data():
    print("IN getData for sensors")
    return jsonify(load_data())



@sensor_data.route('/sensors/readings/', methods=['GET'])
def get_sensor_readings():
    print("Sensor Readings:")

    readings = SensorReadings.query.order_by(SensorReadings.recorded_at)

    sensor_readings = []

    first = True

    sensors = Sensors.query.all()
    sensor_data = {}
    for s in sensors:
        sensor_data[s.sensor_id] = s.sensor_name


    for r in readings:
        next_reading = r.__dict__
        del next_reading["_sa_instance_state"]
        # if (first):
        #     sensor = Sensors.query.get(r.sensor_id)
        #     first = False
        # print("Retrieved Sensor:")
        # print(sensor.__dict__)
        rowData = next_reading
        rowData["sensor_name"] = sensor_data[r.sensor_id]
        sensor_readings.append(rowData)

        print(rowData)

    # print("Sensor Readings:")
    # print(sensor_readings)
    # jsonData = jsonify(sensor_readings)
    # print(jsonData)

    return jsonify(sensor_readings)


@sensor_data.route('/sensors/', methods=['POST',])
def insert_data():
    print("Insert Sensor Request...")
    new_sensor_data = request.json
    print(new_sensor_data)

    # Create the New Sensor

    print(new_sensor_data)

    new_sensor = Sensors(
        sensor_name = new_sensor_data["sensor_name"],
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
        "sensor_name": new_sensor.sensor_name,
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
        "sensor_name" : jsonrequest["sensor_name"],
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
    s_data = Sensor.__dict__
    print(s_data)
    print("Next Sensor: {} {} {}".format(Sensor.sensor_id, Sensor.crops.crop_name, Sensor.bcm_pin))
    sensor = moisturemeter.MoistureMeter(Sensor.sensor_id, Sensor.bcm_pin)
    print("Sensor: ")
    print(sensor)
    sensor_reading_data = sensor.get_kpa_value()

    print(sensor_reading_data)
    return jsonify(sensor_reading_data)


def do_sensor_readings():
    sensors = Sensors.query.all()

    for sensor_data in sensors:
        print("Next Sensor: {} {} {}".format(sensor_data.sensor_id, sensor_data.crops.crop_name, sensor_data.bcm_pin))
        nxt_sensor = moisturemeter.MoistureMeter(sensor_data.sensor_id, sensor_data.bcm_pin)
        print("get kPa for : ", sensor_data.sensor_id)
        sensor_reading_data = nxt_sensor.get_kpa_value()
        print("Return data: ", sensor_reading_data)

        new_reading = SensorReadings(sensor_data.sensor_id, sensor_reading_data)


        x = datetime.datetime.now()
        print("Date:")
        print(x)
        print("New Reading")
        print(new_reading.__dict__)

        db.session.add(new_reading)
        db.session.commit()

def get_sensors():
    sensors = Sensors.query.all()

    return sensors

# Returns the latest count sensor readings for a given sensor id
def get_latest_sensor_readings(sensor_id, count):
    print("in get latest sensor readings")

    readings = SensorReadings.query.filter_by(sensor_id=sensor_id).order_by(SensorReadings.recorded_at.desc()).limit(count)

    return readings
