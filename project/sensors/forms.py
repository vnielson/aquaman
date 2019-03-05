from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddSensorForm(FlaskForm):
    sensor_id = StringField('Sensor ID', validators=[DataRequired()])
    configuration = StringField('Configuration', validators=[DataRequired()])
    crop = StringField('Crop', validators=[DataRequired()])
    valve_id = StringField('Valve ID', validators=[DataRequired()])
    bcm_pin = IntegerField('BCM Pin', validators=[DataRequired()])
    submit = SubmitField('Add Sensor')


class DeleteSensorForm(FlaskForm):
    sensor_id = StringField('Sensor Id', validators=[DataRequired()])
    submit = SubmitField('Delete Sensor')


