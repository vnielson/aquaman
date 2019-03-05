import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)


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


####################################################################
#####################  BLUEPRINT CONFIGS      ######################
####################################################################


from project.core.views import core
from project.crop_data.views import crop_data
from project.sensors.views import sensor_data
from project.valves.views import valve_data

# Register the apps (Blueprints)
app.register_blueprint(core)
app.register_blueprint(crop_data)
app.register_blueprint(sensor_data)
app.register_blueprint(valve_data)



