from flask import render_template, Blueprint, url_for, redirect, jsonify, request
from project import db
from project.models import Valves, WateringEvent
from project.valves import valve
from datetime import datetime

valve_data = Blueprint('valve_data', __name__)


def close_all_valves():
    valves = Valves.query.all()
    for v in valves:
        valve_Instance = valve.valve(v.valve_id, v.relay_controller)
        print("ValveItem: ")
        print(valve_Instance)
        close_valve_status = valve_Instance.close_valve()




def load_data():

    valve_data = []
    valves = Valves.query.all()
    for s in valves:
        next_valve = s.__dict__
        del next_valve["_sa_instance_state"]
        valve_data.append(next_valve)

    print("Valve Data... ")
    print(valve_data)
    return valve_data

@valve_data.route('/valves/', methods=['GET'])
def get_data():
    print("IN getData for valves")
    return jsonify(load_data())



# @valve_data.route('/valves/states/', methods=['GET'])
# def get_valve_readings():
# 
#     readings = ValveReadings.query.all()
# 
#     sensor_readings = []
# 
#     for s in readings:
#         next_reading = s.__dict__
#         del next_reading["_sa_instance_state"]
#         sensor_readings.append(next_reading)
# 
#     print("Valve Readings:")
#     print(sensor_readings)
# 
#     return jsonify(sensor_readings)
# 

@valve_data.route('/valves/', methods=['POST',])
def insert_data():
    print("Insert Valve Request...")
    new_valve_data = request.json
    print(new_valve_data)

    # Create the New Valve

    new_valve = Valves(
        valve_name=new_valve_data["valve_name"],
        relay_controller=new_valve_data["relay_controller"]
        )

    db.session.add(new_valve)
    db.session.commit()



    ret_valve = {
        "valve_id": new_valve.valve_id,
        "valve_name": new_valve.valve_name,
        "relay_controller": new_valve.relay_controller
    }

    return jsonify(ret_valve)
    # return jsonify(success=True)




@valve_data.route('/valves/<int:valve_id>', methods=['PUT',])
def update_valve(valve_id):

    print("UPDATE VALVE:")
    #Find item to update
    jsonrequest = request.json
    print("json request")
    print(jsonrequest)

    valve = db.session.query(Valves).get(jsonrequest["valve_id"]);
    print("Valve to be updated:")
    print(valve)

    update = {
        "relay_controller" : jsonrequest["relay_controller"],
        "valve_name" : jsonrequest["valve_name"]
    }

    print(update)

    db.session.query(Valves).filter_by(valve_id=jsonrequest["valve_id"]).update(update)
    db.session.commit();


    return jsonify(request.json)
    # return jsonify(success=True)


@valve_data.route('/valves/<int:valve_id>', methods=['DELETE',])
def delete_valve(valve_id):

    valve = db.session.query(Valves).get(valve_id);

    del_valve_return = db.session.delete(valve)
    print("Return value  ", del_valve_return)

    db.session.commit()

    return jsonify(success=True)


@valve_data.route('/valves/get_status/<int:valve_id>', methods=['GET'])
def get_valve_status(valve_id):
    print("IN get status for valve:")
    print(valve_id)

    Valve = Valves.query.get(valve_id)
    s_data = Valve.__dict__
    print(s_data)
    print("Next Valve: {} {} {}".format(Valve.valve_id, Valve.valve_name, Valve.relay_controller))
    valve_Instance = valve.valve(Valve.valve_id, Valve.relay_controller)
    print("ValveItem: ")
    print(valve_Instance)
    valve_status = valve_Instance.valve_status()

    ret_data = {}
    ret_data["status"] = valve_status
    print(ret_data)
    return jsonify(ret_data)

@valve_data.route('/valves/open/<int:valve_id>', methods=['GET'])
def open_valve(valve_id):
    print("IN OPEN valve:")
    print(valve_id)

    open_valve_status = open_valve(valve_id)

    print(open_valve_status)
    return jsonify(open_valve_status)

@valve_data.route('/valves/close/<int:valve_id>', methods=['GET'])
def close_valve(valve_id):
    print("IN CLOSE valve:")
    print(valve_id)
    close_valve_status = close_valve(valve_id)
    return jsonify(close_valve_status)


def open_valve(valve_id, record_event, trigger_kpa):
    Valve = Valves.query.get(valve_id)
    s_data = Valve.__dict__
    print(s_data)
    print("Next Valve: {} {} {}".format(Valve.valve_id, Valve.valve_name, Valve.relay_controller))
    valve_Instance = valve.valve(Valve.valve_id, Valve.relay_controller)
    print("ValveItem: ")
    print(valve_Instance)
    open_valve_status = valve_Instance.open_valve()

    def __init__(self, valve_id, water_start, trigger_kpa):
        self.valve_id = valve_id
        self.water_start = water_start
        self.trigger_kpa = trigger_kpa

    watering_event_id = 0
    if (record_event):
        watering_event = WateringEvent(Valve.valve_id, datetime.now(), trigger_kpa)
        db.session.add(watering_event)
        db.session.commit()
        watering_event_id = watering_event.p_key
        print("Record watering event:")
        print(watering_event.__dict__)
        print(watering_event_id)

    ret_status = {}
    ret_status["open_status"] = open_valve_status
    ret_status["event_id"] = watering_event_id

    return ret_status


def close_valve(valve_id, record_event, event_id):
    Valve = Valves.query.get(valve_id)
    s_data = Valve.__dict__
    print(s_data)
    print("Next Valve: {} {} {}".format(Valve.valve_id, Valve.valve_name, Valve.relay_controller))
    valve_Instance = valve.valve(Valve.valve_id, Valve.relay_controller)
    print("ValveItem: ")
    print(valve_Instance)
    close_valve_status = valve_Instance.close_valve()

    print(close_valve_status)
    if (record_event):
        watering_event = WateringEvent.query.get(event_id)
        watering_event.state = "COMPLETE"
        watering_event.water_stop = datetime.now()
        delta_time = (watering_event.water_stop - watering_event.water_start)
        watering_event.open_time = delta_time.total_seconds()
        print("Close Valve, Update Watering Event:")
        print(watering_event.__dict__)
        db.session.commit()

    return close_valve_status
