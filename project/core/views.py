from flask import render_template, request, Blueprint
from project import db
from project.models import Sensors
from project.models import SensorReadings


core = Blueprint('core', __name__)

@core.route('/')
def index():
    # HOMEPAGE DASHBOARD VIEW

    sensors = Sensors.query.all()
    print("DASHBOARD SENSOR_DATA:")
    print(sensors)
    for s in sensors:
        s_data = s.__dict__
        print("Next Sensor:")
        print(s_data)

    return render_template('index.html', sensors=sensors)

