from flask import render_template, Blueprint, url_for, redirect, jsonify, request
from project import db
from project.models import Valves, WateringEvent
from project.core.aqualogger import waterlog

watering_events = Blueprint('watering_events', __name__)



def load_data():

    ret_data = []
    watering_events = WateringEvent.query.order_by(WateringEvent.created.desc())
    valves = Valves.query.all()

    for we in watering_events:
        # waterlog.debug(we)
        next_event = we.__dict__
        # waterlog.debug(next_event)
        del next_event["_sa_instance_state"]
        for valve in valves:
            if valve.valve_id == next_event["valve_id"]:
                next_event["valve_name"] = valve.valve_name

        ret_data.append(next_event)
        # waterlog.debug(ret_data)

    # waterlog.debug("Watering Event Data... ")
    # waterlog.debug(ret_data)
    return ret_data

@watering_events.route('/watering_events/', methods=['GET'])
def get_data():
    waterlog.debug("IN getData for valves")
    return jsonify(load_data())




@watering_events.route('/watering_events/<int:event_id>', methods=['DELETE',])
def delete_watering_event(event_id):

    event = db.session.query(WateringEvent).get(event_id);
    waterlog.debug("Delete Watering Event: ")
    waterlog.debug(event.__dict__)

    del_event_return = db.session.delete(event)
    waterlog.debug("Return del data  ", del_event_return)

    db.session.commit()

    return jsonify(success=True)




