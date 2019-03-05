from flask import render_template, request, Blueprint


core = Blueprint('core', __name__)

@core.route('/')
def index():
    '''
    This is the homepage view.
    '''

    return render_template('index.html')

