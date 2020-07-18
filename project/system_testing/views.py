from flask import render_template, Blueprint, url_for, redirect, jsonify
from project import db
from project.models import Crops
from project.crop_data.forms import AddCropForm, DeleteCropForm
from project.system_operation import system_operations

system_testing = Blueprint('system_testing', __name__)

@system_testing.route('/system_testing')
def index():

    return render_template('system_testing.html')


@system_testing.route('/test_do_watering')
def test_do_watering():

    print("IN TEST DO WATERING")

    system_operations.do_watering(True)

    return jsonify(True)

