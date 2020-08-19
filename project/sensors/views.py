import datetime
from flask import render_template, Blueprint, url_for, redirect, request, jsonify
from project import db
from project.sensors import moisturemeter
from project.models import Sensors
from project.models import SensorReadings
# from project.sensors.forms import AddSensorForm, DeleteSensorForm
from project.core.aqualogger import senlog

sensor_data = Blueprint('sensor_data', __name__)


def load_data():

    senlog.debug("Load Data:")

    sensor_data = []
    sensors = Sensors.query.all()
    for s in sensors:
        next_sensor = s.__dict__
        v_data = s.valves.__dict__
        c_data = s.crops.__dict__
        del next_sensor["_sa_instance_state"]
        senlog.debug(next_sensor)
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

    # senlog.debug("Sensor Data... ")
    # senlog.debug(sensor_data)
    return sensor_data

@sensor_data.route('/sensors/', methods=['GET'])
def get_data():
    senlog.debug("IN getData for sensors")
    return jsonify(load_data())



@sensor_data.route('/sensors/readings', methods=['GET'])
def get_sensor_readings():
    senlog.debug("Sensor Readings:")
    # user = request.args.get('user')
    # senlog.debug(request.args)
    sort_order = request.args.get('sort_order')
    if sort_order is None:
        sort_order = ''

    # senlog.debug("Sort Order: " + sort_order)

    days_to_fetch = request.args.get('days')
    if days_to_fetch is None:
        if (sort_order == 'desc'):
            readings = SensorReadings.query.order_by(SensorReadings.recorded_at.desc())
        else:
            readings = SensorReadings.query.order_by(SensorReadings.recorded_at)
    else:
        filter_after = datetime.datetime.today() - datetime.timedelta(days=int(days_to_fetch))
        if (sort_order == 'desc'):
            readings = SensorReadings.query.filter(SensorReadings.recorded_at >= filter_after).order_by(SensorReadings.recorded_at.desc())
        else:
            readings = SensorReadings.query.filter(SensorReadings.recorded_at >= filter_after).order_by(SensorReadings.recorded_at)

    # payments = Payment.query.filter(Payment.due_date >= filter_after).all()

    # jsonrequest = request.json
    # senlog.debug("json request")
    # senlog.debug(jsonrequest)
    #
    # if jsonrequest:
    #     sort_order = jsonrequest["sort_order"]



    sensor_readings = []

    first = True

    sensors = Sensors.query.all()
    sensor_data = {}
    for s in sensors:
        sensor_data[s.sensor_id] = s.sensor_name

    senlog.debug(sensor_data)

    for r in readings:
        next_reading = r.__dict__
        del next_reading["_sa_instance_state"]
        # if (first):
        #     sensor = Sensors.query.get(r.sensor_id)
        #     first = False
        # senlog.debug("Retrieved Sensor:")
        # senlog.debug(sensor.__dict__)
        # senlog.debug(next_reading)
        if r.sensor_id in sensor_data:
            rowData = next_reading
            rowData["sensor_name"] = sensor_data[r.sensor_id]
            sensor_readings.append(rowData)
        else:
            senlog.warning("Sensor ID NOT FOUND")
            senlog.warning(r.sensor_id)

        # senlog.debug(rowData)

    # senlog.debug("Sensor Readings:")
    # count = 0
    # for reading in sensor_readings:
    #     senlog.debug(reading)
    #     count += 1
    #     if count > 50:
    #         break

    # jsonData = jsonify(sensor_readings)
    # senlog.debug(jsonData)

    return jsonify(sensor_readings)


@sensor_data.route('/sensors/', methods=['POST',])
def insert_data():
    senlog.debug("Insert Sensor Request...")
    new_sensor_data = request.json
    senlog.debug(new_sensor_data)

    # Create the New Sensor

    senlog.debug(new_sensor_data)

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

    senlog.debug("UPDATE SENSOR:")
    #Find item to update
    jsonrequest = request.json
    senlog.debug("json request")
    senlog.debug(jsonrequest)

    sensor = db.session.query(Sensors).get(jsonrequest["sensor_id"]);
    senlog.debug("Sensor to be updated:")
    senlog.debug(sensor)

    update = {
        "sensor_name" : jsonrequest["sensor_name"],
        "configuration" : jsonrequest["configuration"],
        "crop_id": jsonrequest["crop_id"],
        "valve_id": jsonrequest["valve_id"],
        "bcm_pin": jsonrequest["bcm_pin"]
    }

    senlog.debug(update)

    db.session.query(Sensors).filter_by(sensor_id=jsonrequest["sensor_id"]).update(update)
    db.session.commit();


    return jsonify(request.json)
    # return jsonify(success=True)


@sensor_data.route('/sensors/<int:sensor_id>', methods=['DELETE',])
def delete_sensor(sensor_id):

    sensor = db.session.query(Sensors).get(sensor_id);

    del_school_return = db.session.delete(sensor)
    senlog.debug("Return value  ", del_school_return)

    db.session.commit()

    return jsonify(success=True)


@sensor_data.route('/sensors/get_reading/<int:sensor_id>', methods=['GET'])
def get_sensor_reading(sensor_id):
    senlog.debug("IN getreading for sensor:")
    senlog.debug(sensor_id)

    sensor_reading_data = get_sensor_reading(sensor_id)
    senlog.debug(sensor_reading_data)
    return jsonify(sensor_reading_data)


def do_sensor_readings():
    sensors = Sensors.query.all()

    for sensor_data in sensors:
        senlog.info("Next Sensor: {} {} {}".format(sensor_data.sensor_id, sensor_data.crops.crop_name, sensor_data.bcm_pin))
        nxt_sensor = moisturemeter.MoistureMeter(sensor_data.sensor_id, sensor_data.bcm_pin)
        # senlog.debug("get kPa for : ", sensor_data.sensor_id)
        sensor_reading_data = nxt_sensor.get_kpa_value()
        senlog.info("Return data: ", sensor_reading_data)
        if (not sensor_reading_data["data_valid"]):
            senlog.error("Sensor reading returned DATA VALID as FALSE")

        new_reading = SensorReadings(sensor_data.sensor_id, sensor_reading_data)

        x = datetime.datetime.now()
        senlog.debug("Date:")
        senlog.debug(x)
        senlog.debug("New Reading")
        senlog.debug(new_reading.__dict__)

        db.session.add(new_reading)
        db.session.commit()

def get_sensors():
    sensors = Sensors.query.all()

    return sensors

# Returns the latest count sensor readings for a given sensor id
def get_latest_sensor_readings(sensor_id, count):
    senlog.debug("in get latest sensor readings")

    readings = SensorReadings.query.filter_by(sensor_id=sensor_id).order_by(SensorReadings.recorded_at.desc()).limit(count)

    return readings

def get_sensor_reading(sensor_id):
    Sensor = Sensors.query.get(sensor_id)
    s_data = Sensor.__dict__
    # senlog.debug(s_data)
    # senlog.debug("Next Sensor: {} {} {}".format(Sensor.sensor_id, Sensor.crops.crop_name, Sensor.bcm_pin))
    sensor = moisturemeter.MoistureMeter(Sensor.sensor_id, Sensor.bcm_pin)
    # senlog.debug("Sensor: ")
    # senlog.debug(sensor)
    sensor_reading_data = sensor.get_kpa_value()

    return sensor_reading_data
