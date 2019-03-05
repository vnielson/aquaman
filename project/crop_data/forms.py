from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddCropForm(FlaskForm):
    crop = StringField('Crop', validators=[DataRequired()])
    ideal_kpa = IntegerField('Ideal_KPa', validators=[DataRequired()])
    dry_kpa = IntegerField('Dry_KPa', validators=[DataRequired()])
    saturated_kpa = IntegerField('Saturated_KPa', validators=[DataRequired()])
    submit = SubmitField('Add Crop')


class DeleteCropForm(FlaskForm):
    crop = StringField('Crop Name', validators=[DataRequired()])
    submit = SubmitField('Delete Crop')


