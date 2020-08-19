from flask import render_template, request, Blueprint
from project.models import Sensors
from project.core.aqualogger import corelog

core = Blueprint('core', __name__)

@core.route('/')
def index():
    # HOMEPAGE DASHBOARD VIEW

    sensors = Sensors.query.all()
    corelog.debug("DASHBOARD SENSOR_DATA:")
    corelog.debug(sensors)
    for s in sensors:
        s_data = s.__dict__
        corelog.debug("Next Sensor:")
        corelog.debug(s_data)

    return render_template('index.html', sensors=sensors)

