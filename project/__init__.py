import os
import datetime
#from datetime import timezone
import time
#import pytz

# from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.json import JSONEncoder
from datetime import date
from project.core.aqualogger import aqlog



class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()

        return super().default(o)

class MyFlask(Flask):
    json_encoder = MyJSONEncoder

app = MyFlask(__name__)
# app = Flask(__name__)

# asdfdsf
####################################################################
##################### CONFIGURATION           ######################
####################################################################

app.config['SECRET_KEY'] = 'itsasecret'


####################################################################
#####################  DATABASE SETUP         ######################
####################################################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""

    aqlog.debug(value)
    return value.strftime(format)

####################################################################
#####################  BLUEPRINT CONFIGS      ######################
####################################################################


from project.core.views import core
from project.crop_data.views import crop_data
from project.sensors.views import sensor_data
from project.valves.views import valve_data
from project.wateringevents.views import watering_events
from project.system_operation import system_operations
from project.system_testing.views import system_testing
from project.logviewer.views import log_viewer
from project.weather.views import weather

# Register the apps (Blueprints)
app.register_blueprint(core)
app.register_blueprint(crop_data)
app.register_blueprint(sensor_data)
app.register_blueprint(valve_data)
app.register_blueprint(watering_events)
app.register_blueprint(system_testing)
app.register_blueprint(log_viewer)
app.register_blueprint(weather)

# Initialize the System
if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    system_operations.initialize_system()
    system_operations.initialize_scheduler()

