from flask import render_template, Blueprint, url_for, redirect, jsonify, request
from project import db
from project.models import Valves, WateringEvent
from project.valves import valve
from datetime import datetime

watering_events = Blueprint('watering_events', __name__)



def load_data():

    ret_data = []
    watering_events = WateringEvent.query.all()
    for we in watering_events:
        # print(we)
        next_event = we.__dict__
        # print(next_event)
        del next_event["_sa_instance_state"]
        ret_data.append(next_event)
        # print(ret_data)

    # print("Watering Event Data... ")
    # print(ret_data)
    return ret_data

@watering_events.route('/watering_events/', methods=['GET'])
def get_data():
    print("IN getData for valves")
    return jsonify(load_data())




@watering_events.route('/watering_events/<int:event_id>', methods=['DELETE',])
def delete_watering_event(event_id):

    event = db.session.query(WateringEvent).get(event_id);
    print("Delete Watering Event: ")
    print(event.__dict__)

    del_event_return = db.session.delete(event)
    print("Return del data  ", del_event_return)

    db.session.commit()

    return jsonify(success=True)




