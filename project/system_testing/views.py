from flask import render_template, Blueprint, url_for, redirect, jsonify
from project.system_operation import system_operations
from project.core.aqualogger import systestlog

system_testing = Blueprint('system_testing', __name__)

@system_testing.route('/system_testing')
def index():

    return render_template('system_testing.html')


@system_testing.route('/test_do_watering')
def test_do_watering():

    systestlog.debug("IN TEST DO WATERING")

    system_operations.do_watering(True)

    return jsonify(True)

