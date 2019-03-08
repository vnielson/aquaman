from flask import render_template, Blueprint, url_for, redirect
from project import db
from project.models import Sensor_Info
from project.models import SensorReadings
from project.sensors.forms import AddSensorForm, DeleteSensorForm

sensor_data = Blueprint('sensor_data', __name__)

@sensor_data.route('/sensor/list')
def list_sensor_data():

    sensors = Sensor_Info.query.all()
    print("IN SENSOR_DATA:")
    print(sensors)
    return render_template('list_sensor_data.html', sensors=sensors)


@sensor_data.route('/sensor/add', methods=['GET','POST'])
def add_sensor_data():

    form = AddSensorForm()

    if form.validate_on_submit():
        sensor_id = form.sensor_id.data
        configuration = form.configuration.data
        crop = form.crop.data
        valve_id = form.valve_id.data
        bcm_pin = form.bcm_pin.data

        new_sensor = Sensor_Info(sensor_id, configuration, crop, valve_id, bcm_pin)
        db.session.add(new_sensor)
        db.session.commit()
        return redirect(url_for('sensor_data.list_sensor_data'))

    return render_template('add_sensor_data.html', form=form)


@sensor_data.route('/sensor/delete', methods=['GET','POST'])
def delete_sensor_data():

    form = DeleteSensorForm()

    if form.validate_on_submit():
        sensor_id = form.sensor_id.data
        sensor = Sensor_Info.query.get(sensor_id)
        db.session.delete(sensor)
        db.session.commit()

        return redirect(url_for('sensor_data.list_sensor_data'))

    return render_template('delete_sensor_data.html', form=form)



@sensor_data.route('/sensorreadings/list')
def list_sensor_readings():

    readings = SensorReadings.query.all()
    return render_template('list_sensor_readings.html', readings=readings)


