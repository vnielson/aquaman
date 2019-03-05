from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddValveForm(FlaskForm):
    valve_id = StringField('Valve ID', validators=[DataRequired()])
    bcm_pin = IntegerField('BCM Pin', validators=[DataRequired()])
    submit = SubmitField('Add Valve')


class DeleteValveForm(FlaskForm):
    valve_id = StringField('Valve Id', validators=[DataRequired()])
    submit = SubmitField('Delete Valve')


