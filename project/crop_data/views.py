from flask import render_template, Blueprint, url_for, redirect
from project import db
from project.models import Crop_Info
from project.crop_data.forms import AddCropForm, DeleteCropForm

crop_data = Blueprint('crop_data', __name__)

@crop_data.route('/crop/list')
def list_crop_data():

    crops = Crop_Info.query.all()
    print("crops[1] {}   {}".format(crops[1].crop,crops[1].dry_kpa))
    crops1 = [{"name":"Tomatoes", "ideal_kpa":"33"},{"name":"Peppers", "ideal_kpa":"43"}]
    print("CROPS:")
    print (crops)
    return render_template('list_crop_data.html', crops=crops)


@crop_data.route('/crop/add', methods=['GET','POST'])
def add_crop_data():

    form = AddCropForm()

    if form.validate_on_submit():
        crop = form.crop.data
        ideal_kpa = form.ideal_kpa.data
        dry_kpa = form.dry_kpa.data
        saturated_kpa = form.saturated_kpa.data
        new_crop = Crop_Info(crop, ideal_kpa, dry_kpa, saturated_kpa)
        db.session.add(new_crop)
        db.session.commit()
        return redirect(url_for('crop_data.list_crop_data'))

    return render_template('add_crop_data.html', form=form)


@crop_data.route('/crop/delete', methods=['GET','POST'])
def delete_crop_data():

    form = DeleteCropForm()

    if form.validate_on_submit():
        crop_name = form.crop.data
        crop = Crop_Info.query.get(crop_name)
        db.session.delete(crop)
        db.session.commit()

        return redirect(url_for('crop_data.list_crop_data'))

    return render_template('delete_crop_data.html', form=form)

