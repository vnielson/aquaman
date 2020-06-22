from flask import render_template, Blueprint, url_for, redirect
from project import db
from project.models import Crops
from project.crop_data.forms import AddCropForm, DeleteCropForm

system_testing = Blueprint('system_testing', __name__)

@system_testing.route('/system_testing')
def index():

    return render_template('system_testing.html')


