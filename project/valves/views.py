from flask import render_template, Blueprint, url_for, redirect
from project import db
from project.models import Valve_Info
from project.valves.forms import AddValveForm, DeleteValveForm

valve_data = Blueprint('valve_data', __name__)

@valve_data.route('/valve/list')
def list_valve_data():

    valves = Valve_Info.query.all()
    return render_template('list_valve_data.html', valves=valves)


@valve_data.route('/valve/add', methods=['GET','POST'])
def add_valve_data():

    form = AddValveForm()

    if form.validate_on_submit():
        valve_id = form.valve_id.data
        bcm_pin = form.bcm_pin.data
        new_valve = Valve_Info(valve_id, bcm_pin)
        db.session.add(new_valve)
        db.session.commit()
        return redirect(url_for('valve_data.list_valve_data'))

    return render_template('add_valve_data.html', form=form)


@valve_data.route('/valve/delete', methods=['GET','POST'])
def delete_valve_data():

    form = DeleteValveForm()

    if form.validate_on_submit():
        valve_id = form.valve_id.data
        valve = Valve_Info.query.get(valve_id)
        db.session.delete(valve)
        db.session.commit()

        return redirect(url_for('valve_data.list_valve_data'))

    return render_template('delete_valve_data.html', form=form)

