from flask import render_template, Blueprint, url_for, redirect, jsonify, request
from project import db
from project.models import Crops
from project.crop_data.forms import AddCropForm, DeleteCropForm
from project.core.aqualogger import logviewerlog

log_viewer = Blueprint('log_viewer', __name__)



@log_viewer.route('/log_viewer/', methods=['GET'])
def get_data():
    logviewerlog.debug("IN getData for crops")
    return render_template('logviewer.html')



